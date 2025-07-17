import re
from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError


def parse_gs1_barcode(barcode_str):
    pattern = r"\((\d{2})\)([^\(]+)"
    return {ai: value.strip() for ai, value in re.findall(pattern, barcode_str)}


class StockBarcodeTransferWizard(models.TransientModel):
    _name = "stock.barcode.transfer.wizard"
    _description = "Barcode Transfer Wizard"

    location_id = fields.Many2one("stock.location", string="Source Location")
    allowed_location_ids = fields.Many2many(
        "stock.location",
        compute="_compute_allowed_locations",
        string="Allowed Locations",
    )
    barcode = fields.Char(string="Scan Barcode")

    scanned_line_ids = fields.One2many(
        "stock.barcode.transfer.line", "wizard_id", string="Scanned Lines"
    )

    @api.depends("scanned_line_ids")
    def _compute_allowed_locations(self):
        for wizard in self:
            wizard.allowed_location_ids = [
                (6, 0, wizard.scanned_line_ids.mapped("location_id").ids)
            ]

    @api.onchange("barcode")
    def _onchange_barcode(self):
        if not self.barcode:
            return

        gs1_data = parse_gs1_barcode(self.barcode)
        product_code = gs1_data.get("01")
        lot_name = gs1_data.get("10")
        expiration_raw = gs1_data.get("17")

        if not product_code:
            raise UserError(_("Barcode does not contain a valid (01) product code."))

        expiration_date = None
        if expiration_raw and re.match(r"^\d{6}$", expiration_raw):
            try:
                expiration_date = datetime.strptime(expiration_raw, "%y%m%d").date()
            except ValueError as err:
                raise UserError(_("Invalid expiration date format.")) from err

        Product = self.env["product.product"]
        Lot = self.env["stock.lot"]
        Quant = self.env["stock.quant"]

        product = Product.search(
            ["|", ("barcode", "=", product_code), ("default_code", "=", product_code)],
            limit=1,
        )

        if not product:
            raise UserError(_("No product found with code %s.") % product_code)

        lot = Lot.search(
            [("product_id", "=", product.id), ("name", "=", lot_name)], limit=1
        )

        if not lot:
            raise UserError(
                _("No lot '%(lot)s' found for product '%(product)s.")
                % {
                    "lot": lot_name,
                    "product": product.display_name,
                }
            )

        quants = Quant.search(
            [
                ("product_id", "=", product.id),
                ("lot_id", "=", lot.id),
                ("quantity", ">", 0),
            ]
        )

        if not quants:
            raise UserError(
                _("No stock available for product '%(product)s' lot '%(lot)s.")
                % {
                    "product": product.display_name,
                    "lot": lot.name,
                }
            )

        for quant in quants:
            self.write(
                {
                    "scanned_line_ids": [
                        (
                            0,
                            0,
                            {
                                "product_id": product.id,
                                "lot_id": lot.id,
                                "lot_name": lot.name,
                                "expiration_date": expiration_date,
                                "location_id": quant.location_id.id,
                            },
                        )
                    ]
                }
            )

        self.barcode = ""

    def action_create_picking(self):
        self.ensure_one()
        if not self.location_id:
            raise UserError(
                _("Please select the source location before creating the transfer.")
            )

        Picking = self.env["stock.picking"]
        Move = self.env["stock.move"]

        picking = Picking.create(
            {
                "partner_id": self.env.user.partner_id.id,
                "picking_type_id": self.env.ref("stock.picking_type_internal").id,
                "location_id": self.location_id.id,
                "location_dest_id": self.env.user.partner_id.property_stock_customer.id,
                "move_type": "direct",
            }
        )

        lines_created = []

        for line in self.scanned_line_ids.filtered(
            lambda li: li.location_id == self.location_id
        ):
            Move.create(
                {
                    "picking_id": picking.id,
                    "name": line.product_id.display_name,
                    "product_id": line.product_id.id,
                    "product_uom_qty": 1.0,
                    "product_uom": line.product_id.uom_id.id,
                    "location_id": self.location_id.id,
                    "location_dest_id": (
                        self.env.user.partner_id.property_stock_customer.id
                    ),
                }
            )

            # Tallenna rivin tiedot viestiä varten
            lines_created.append(
                _("- %(product)s")
                % {
                    "product": line.product_id.display_name,
                }
            )

        # Muodosta viesti ilman HTML-tageja
        body = _(
            "Stock picking was created using the Barcode Transfer Wizard by"
            " %(user)s from source"
            " location '%(location)s'.\n\nScanned lines:\n%(lines)s"
        ) % {
            "user": self.env.user.name,
            "location": self.location_id.display_name,
            "lines": "\n".join(lines_created),
        }

        picking.message_post(body=body, subtype_xmlid="mail.mt_comment")

        return {
            "type": "ir.actions.act_window",
            "res_model": "stock.picking",
            "res_id": picking.id,
            "view_mode": "form",
            "target": "current",
        }


class StockBarcodeTransferLine(models.TransientModel):
    _name = "stock.barcode.transfer.line"
    _description = "Scanned Transfer Line"

    wizard_id = fields.Many2one(
        "stock.barcode.transfer.wizard", required=True, ondelete="cascade"
    )
    product_id = fields.Many2one("product.product", required=True)
    lot_id = fields.Many2one("stock.lot", readonly=True)
    lot_name = fields.Char(readonly=True)
    expiration_date = fields.Date(readonly=True)
    location_id = fields.Many2one(
        "stock.location", required=True, domain=[("usage", "=", "internal")]
    )
