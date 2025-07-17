import logging
import re
from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


def parse_gs1_barcode(barcode_str):
    pattern = r"\((\d{2})\)([^\(]+)"
    return {ai: value.strip() for ai, value in re.findall(pattern, barcode_str)}


class QuantBarcodeUpdateWizard(models.TransientModel):
    _name = "quant.barcode.update.wizard"
    _description = "Quant Barcode Update Wizard"

    barcode = fields.Char(string="Scan Barcode")
    scanned_line_ids = fields.One2many(
        "quant.barcode.update.line", "wizard_id", string="Scanned Lines"
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
            raise UserError(_("No product found for barcode %s.") % product_code)

        lot = Lot.search(
            [("product_id", "=", product.id), ("name", "=", lot_name)], limit=1
        )

        if not lot:
            raise UserError(
                _("Lot '%(lot)s' not found for product '%(product)s'.")
                % {"lot": lot_name, "product": product.display_name}
            )

        # Tarkistetaan että quant löytyy kyseisestä sijainnista
        quant = Quant.search(
            [
                ("product_id", "=", product.id),
                ("lot_id", "=", lot.id),
            ],
            limit=1,
        )

        if not quant:
            raise UserError(
                _("No stock found for product '%(product)s'.")
                % {
                    "product": product.display_name,
                }
            )

        already = self.scanned_line_ids.filtered(
            lambda li: li.product_id == product and li.lot_id == lot
        )
        if already:
            raise UserError(
                _("Lot '%(lot)s' for product '%(product)s' already scanned.")
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
                            "lot_name": lot.name,
                            "expiration_date": expiration_date,
                            "lot_id": lot.id,
                        },
                    )
                ]
            }
        )

        self.barcode = ""

    def action_apply(self):
        self.ensure_one()
        Quant = self.env["stock.quant"]

        for line in self.scanned_line_ids:
            quant = Quant.search(
                [
                    ("product_id", "=", line.product_id.id),
                    ("lot_id", "=", line.lot_id.id),
                ],
                limit=1,
            )

            if not quant:
                raise UserError(
                    _(
                        "No stock quant found"
                        " for product '%(product)s' and lot '%(lot)s'."
                    )
                    % {
                        "product": line.product_id.display_name,
                        "lot": line.lot_id.name,
                    }
                )

            quant.inventory_quantity = line.quantity
            quant.action_apply_inventory()

        return {"type": "ir.actions.act_window_close"}


class QuantBarcodeUpdateLine(models.TransientModel):
    _name = "quant.barcode.update.line"
    _description = "Scanned Quant Line"

    wizard_id = fields.Many2one(
        "quant.barcode.update.wizard", required=True, ondelete="cascade"
    )
    product_id = fields.Many2one("product.product", required=True)
    lot_id = fields.Many2one("stock.lot", required=True)
    lot_name = fields.Char(readonly=True)
    expiration_date = fields.Date(readonly=True)
    quantity = fields.Float(required=True, default=1.0)
