import logging
import re
from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


def parse_gs1_barcode(barcode_str):
    pattern = r"\((\d{2})\)([^\(]+)"
    matches = re.findall(pattern, barcode_str)
    return {ai: value.strip() for ai, value in matches}


class BarcodeScanWizard(models.TransientModel):
    _name = "barcode.scan.wizard"
    _description = "Barcode Scan Wizard"

    picking_id = fields.Many2one("stock.picking", required=True)
    barcode = fields.Char(string="Scan Barcode")

    scanned_line_ids = fields.One2many(
        "barcode.scan.line", "wizard_id", string="Scanned Lines"
    )

    @api.onchange("barcode")
    def _onchange_barcode(self):
        if not self.barcode:
            return

        gs1_data = parse_gs1_barcode(self.barcode)
        product_code = gs1_data.get("01")
        lot_name = gs1_data.get("10")
        expiration_raw = gs1_data.get("17")

        if not product_code:
            raise UserError(
                _("The barcode does not contain the (01) product identifier.")
            )

        expiration_date = None
        if expiration_raw and re.match(r"^\d{6}$", expiration_raw):
            try:
                expiration_date = datetime.strptime(expiration_raw, "%y%m%d").date()
            except ValueError as err:
                raise UserError(
                    _("The expiration date in the barcode is invalid.")
                ) from err

        product = self.env["product.product"].search(
            [
                "|",
                ("barcode", "=", product_code),
                ("default_code", "=", product_code),
            ],
            limit=1,
        )

        if not product:
            raise UserError(_("No product found with barcode %s.") % product_code)

        moves = self.picking_id.move_ids_without_package.filtered(
            lambda mo: mo.product_id == product
        )
        if not moves:
            raise UserError(
                _("The product '%s' is not in the current transfer.")
                % product.display_name
            )

        lot = self.env["stock.lot"].search(
            [("product_id", "=", product.id), ("name", "=", lot_name)], limit=1
        )

        if not lot:
            raise UserError(
                _("Product found in transfer, but no lot with name '%s' was found.")
                % lot_name
            )

        already_scanned = self.scanned_line_ids.filtered(
            lambda li: li.product_id == product and li.lot_id == lot
        )
        if already_scanned:
            raise UserError(
                _("Lot '%(lot)s' for product '%(product)s' has already been scanned.")
                % {"lot": lot.name, "product": product.display_name}
            )

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
                        },
                    )
                ]
            }
        )

        self.barcode = (
            ""
        )  # tyhjennetään kenttä automaattisesti seuraavaa skannausta varten

    def action_save_lines(self):
        self.ensure_one()

        for line in self.scanned_line_ids:
            move = self.picking_id.move_ids_without_package.filtered(
                lambda mo, line=line: mo.product_id == line.product_id
            )
            if not move:
                raise UserError(
                    _("No stock move found for product %s.")
                    % line.product_id.display_name
                )

            self.env["stock.move.line"].create(
                {
                    "picking_id": self.picking_id.id,
                    "move_id": move.id,
                    "company_id": self.picking_id.company_id.id,
                    "product_id": line.product_id.id,
                    "product_uom_id": move.product_uom.id,
                    "quantity": 1.0,
                    "lot_id": line.lot_id.id,
                    "lot_name": line.lot_name,
                    "expiration_date": line.expiration_date,
                    "location_id": self.picking_id.location_id.id,
                    "location_dest_id": self.picking_id.location_dest_id.id,
                    "date": fields.Datetime.now(),
                }
            )


class BarcodeScanLine(models.TransientModel):
    _name = "barcode.scan.line"
    _description = "Scanned Barcode Line"

    wizard_id = fields.Many2one(
        "barcode.scan.wizard", required=True, ondelete="cascade"
    )
    product_id = fields.Many2one(
        "product.product",
        string="Product",
    )
    lot_id = fields.Many2one("stock.lot", string="Lot", readonly=True)
    lot_name = fields.Char(string="Lot/SN", readonly=True)
    expiration_date = fields.Date(string="Expiration", readonly=True)
