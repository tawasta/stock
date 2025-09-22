import logging
import re
from datetime import datetime

from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


def parse_gs1_barcode(barcode_str):
    pattern = r"\((\d{2})\)([^\(]+)"
    return {ai: value.strip() for ai, value in re.findall(pattern, barcode_str)}


class StockBarcodeTransferWizard(models.TransientModel):
    _name = "stock.barcode.transfer.wizard"
    _description = "Barcode Transfer Wizard"

    picking_type_id = fields.Many2one(comodel_name="stock.picking.type")
    wizard_mode = fields.Selection(related="picking_type_id.code")

    current_product_id = fields.Many2one("product.product", string="Current Product")
    current_lot_id = fields.Many2one("stock.lot", string="Current Lot")
    current_expiry_date = fields.Date()

    location_src_id = fields.Many2one(
        "stock.location", string="Source Location", check_company=True
    )
    location_dest_id = fields.Many2one(
        "stock.location", string="Destination Location", check_company=True
    )

    picking_id = fields.Many2one("stock.picking")

    allowed_location_src_ids = fields.Many2many(
        "stock.location",
        compute="_compute_allowed_src_locations",
        string="Allowed Source Locations",
    )
    allowed_location_dest_ids = fields.Many2many(
        "stock.location",
        compute="_compute_allowed_dest_locations",
        string="Allowed Destination Locations",
    )
    barcode = fields.Char(string="Scan Barcode")

    scanned_line_ids = fields.One2many(
        "stock.barcode.transfer.wizard.line", "wizard_id", string="Scanned Lines"
    )

    info_message = fields.Text(string="Info", readonly=True)
    success_message = fields.Text(string="Success", readonly=True)

    scanned_barcodes = fields.One2many(
        "stock.barcode.transfer.wizard.tmp.line",
        "wizard_id",
        string="Temporary Scanned Barcodes",
    )

    # region Onchange Handlers
    @api.onchange("wizard_mode")
    def _compute_wizard_mode(self):
        if self.wizard_mode == "incoming":
            # Incoming transfers come from supplier location
            self.location_src_id = (
                self.location_src_id or self.env.user.partner_id.property_stock_supplier
            )
        elif self.wizard_mode == "outgoing":
            # Outgoing transfers go to customer location
            self.location_dest_id = (
                self.location_dest_id
                or self.env.user.partner_id.property_stock_customer
            )

    @api.depends("scanned_line_ids")
    def _compute_allowed_src_locations(self):
        for wizard in self:
            wizard.allowed_location_src_ids = [
                (6, 0, wizard.scanned_line_ids.mapped("location_src_id").ids)
            ]

    @api.onchange("location_src_id")
    def _onchange_location_src_id(self):
        if self.location_src_id:
            for line in self.scanned_line_ids:
                line.location_src_id = self.location_src_id

    @api.depends("scanned_line_ids")
    def _compute_allowed_dest_locations(self):
        stock_location = self.env["stock.location"]
        for wizard in self:
            if wizard.wizard_mode in ("incoming", "internal"):
                locations = stock_location.search([("usage", "=", "internal")])
            elif wizard.wizard_mode == "outgoing":
                locations = stock_location.search([("usage", "=", "customer")])
            else:
                raise UserError(_("Invalid wizard mode: %s") % wizard.wizard_mode)

            wizard.allowed_location_dest_ids = [(6, 0, locations.ids)]

    @api.onchange("barcode")
    def _onchange_barcode(self):
        """When changing barcode, parse contents to scanned product lines"""

        # Clear success message
        self.success_message = False
        if not self.barcode:
            return False

        parsed_barcode = parse_gs1_barcode(self.barcode)
        _logger.debug("Parsed barcode: %s", parsed_barcode)
        self.barcode = False

        product_code = parsed_barcode.get("01")
        lot_name = parsed_barcode.get("10")
        expiration_raw = parsed_barcode.get("17")

        expiration_date = self._get_expiration_date(expiration_raw)
        product = self._get_product(product_code)
        lot = self._get_lot(product, lot_name)

        # Update the current values
        current_vals = {
            "current_product_id": product and product.id,
            "current_lot_id": lot and lot.id,
            "current_expiry_date": expiration_date,
        }
        _logger.debug(current_vals)
        self.write(current_vals)

        if self._check_missing_values():
            return False

        quants = self._get_quants()

        if quants:
            if self.wizard_mode == "incoming":
                source_loc = self.location_src_id
            else:
                source_loc = quants[0].location_id.id

            scanned_values = {
                "product_id": product.id,
                "lot_id": lot and lot.id,
                "expiration_date": expiration_date,
                "location_src_id": source_loc,
            }
            self.write({"scanned_line_ids": [Command.create(scanned_values)]})

        # Set success message
        success_message = _(
            "Product '%(product_name)s' with lot '%(lot_name)s' added successfully."
        ) % {
            "product_name": product.display_name,
            "lot_name": lot.name if lot else "",
        }
        _logger.debug(success_message)
        self.success_message = success_message

        # Clear current values
        self.write(
            {
                "current_product_id": False,
                "current_lot_id": False,
                "current_expiry_date": False,
            }
        )

        older_quants = self._get_older_quants(product, quants)

        bypass_check = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("bypass_older_quants_check")
        )

        if older_quants and self.wizard_mode != "incoming" and not bypass_check:
            locations = ", ".join([q.location_id.display_name for q in older_quants])
            message = (
                "The product {product} has stock in {location} that expires sooner. "
                "Please use it first.".format(
                    product=product.display_name,
                    location=locations,
                )
            )
            return {
                "warning": {
                    "title": "Older stock found",
                    "message": message,
                }
            }

    # endregion

    # region Getters
    def _get_older_quants(self, product, quants):
        other_quants = self.env["stock.quant"].search(
            [
                ("product_id", "=", product.id),
                ("quantity", ">", 0),
            ]
        )

        other_quants = other_quants - quants
        found_quants = []

        for quant in other_quants:
            other_date = quant.lot_id.expiration_date
            if any(q.lot_id.expiration_date > other_date for q in quants):
                found_quants.append(quant)
        return found_quants

    def _get_expiration_date(self, expiration_raw):
        if expiration_raw and re.match(r"^\d{6}$", expiration_raw):
            try:
                return datetime.strptime(expiration_raw, "%y%m%d").date()
            except ValueError as err:
                raise UserError(_("Invalid expiration date format.")) from err
        return None

    def _get_product(self, product_code):
        product = self.env["product.product"].search(
            ["|", ("barcode", "=", product_code), ("default_code", "=", product_code)],
            limit=1,
        )

        if not product:
            raise UserError(_("No product found with code %s.") % product_code)

        if not product.tracking == "lot":
            raise UserError(_("Product is not tracked by lot."))

        _logger.debug("Found product: %s", product)

        return product

    def _get_lot(self, product, lot_name):
        if not lot_name:
            return False

        lot = self.env["stock.lot"].search(
            [("product_id", "=", product.id), ("name", "=", lot_name)],
            limit=1,
        )

        if not lot:
            raise UserError(_("No lot found with name %s.") % lot_name)

        _logger.debug("Found lot: %s", lot)

        # Outgoing moves need a lot
        if self.wizard_mode in ["outgoing", "internal"] and not lot:
            raise UserError(
                _("Lot '%(lot)s' not found for product '%(product)s'.")
                % {"lot": lot_name, "product": product.display_name}
            )

        return lot

    def _get_quants(self):
        product = self.current_product_id
        lot = self.current_lot_id

        quants = lot.quant_ids.filtered(lambda q: q.location_id.usage == "internal")

        if self.wizard_mode != "incoming":
            quants = quants.filtered(lambda q: q.quantity > 0)

        _logger.debug("Found quants: %s", quants)

        if not quants and self.wizard_mode != "incoming":
            raise UserError(
                _("No stock available for product '%(product)s' lot '%(lot)s'.")
                % {
                    "product": product.display_name,
                    "lot": lot.name,
                }
            )
        return quants

    # endregion

    def _check_missing_values(self):
        """Check for any missing values"""
        missing = []
        if not self.current_product_id:
            missing.append("(01) product code")
        if not self.current_lot_id:
            missing.append("(10) lot number")

        if missing:
            self.info_message = _("Waiting for: ") + ", ".join(missing)
        else:
            self.info_message = ""

        return missing

    # region Actions
    def _check_missing_picking_values(self):
        _logger.debug("Checking for missing wizard values")
        if not self.scanned_line_ids:
            raise UserError(
                _(
                    "No scanned lines to apply."
                    " Please scan at least one product before saving."
                )
            )

        if self.wizard_mode == "incoming" and not self.location_src_id:
            raise UserError(_("Please select the source location."))

        if not self.location_dest_id:
            raise UserError(_("Please select the destination location."))

    def action_create_picking(self):
        _logger.debug("Creating stock picking from transfer wizard")
        picking_values = {
            "partner_id": self.env.user.partner_id.id,
            "picking_type_id": self.picking_type_id.id,
            "location_id": self.location_src_id.id,
            "location_dest_id": self.location_dest_id.id,
            "move_type": "direct",
        }
        _logger.debug("Creating stock picking with values: %s", picking_values)

        return self.env["stock.picking"].create(picking_values)

    def action_create_moves(self, picking):
        _logger.debug("Creating stock moves from transfer wizard")
        lines_created = []

        # TODO: filter only lines that have a matching location?
        # scanned_line_ids = self.scanned_line_ids.filtered(
        # lambda li: li.location_src_id == self.location_src_id)
        scanned_line_ids = self.scanned_line_ids

        for line in scanned_line_ids:
            location_src_id = line.location_src_id or self.location_src_id

            move_values = {
                "picking_id": picking.id,
                "name": line.product_id.display_name,
                "product_id": line.product_id.id,
                "product_uom_qty": line.quantity,
                "product_uom": line.product_id.uom_id.id,
                "location_id": location_src_id.id,
                "location_dest_id": self.location_dest_id.id,
            }
            _logger.debug("Creating stock move with values: %s", move_values)
            stock_move = self.env["stock.move"].create(move_values)

            move_line_values = {
                "picking_id": picking.id,
                "move_id": stock_move.id,
                "company_id": picking.company_id.id,
                "product_id": line.product_id.id,
                "product_uom_id": stock_move.product_uom.id,
                "quantity": line.quantity,
                "lot_id": line.lot_id.id,
                "lot_name": line.lot_id.name,
                "expiration_date": line.expiration_date,
                "location_id": picking.location_id.id,
                "location_dest_id": picking.location_dest_id.id,
                "date": fields.Datetime.now(),
            }
            _logger.debug("Creating stock move line with values: %s", move_line_values)
            self.env["stock.move.line"].create(move_line_values)

            # Adds line information for the message
            lines_created.append(
                _("- %(product)s")
                % {
                    "product": line.product_id.display_name,
                }
            )

        return lines_created

    def action_confirm(self):
        """Creates a picking from scanned products.
        This is the 'Confirm Transfer' -button"""

        _logger.debug("Confirming stock transfer from transfer wizard")
        self.ensure_one()

        if not self.location_src_id:
            raise UserError(_("Select a source location to confirm the transfer."))

        self._check_missing_picking_values()

        picking = self.action_create_picking()
        move_ids = self.action_create_moves(picking)

        picking.action_confirm()

        # Compose a message without HTML-tags
        body = _(
            "Stock picking was created using the Barcode Transfer Wizard by"
            " %(user)s from source"
            " location '%(location)s'.\n\nScanned lines:\n%(lines)s"
        ) % {
            "user": self.env.user.name,
            "location": self.location_src_id.display_name,
            "lines": "\n".join(move_ids),
        }

        picking.message_post(body=body, subtype_xmlid="mail.mt_comment")

        return {
            "type": "ir.actions.act_window",
            "res_model": "stock.picking",
            "res_id": picking.id,
            "view_mode": "form",
            "target": "current",
        }

    # endregion
