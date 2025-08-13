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
    info_message = fields.Text(string="Info", readonly=True)
    scanned_line_ids = fields.One2many(
        "quant.barcode.update.line", "wizard_id", string="Scanned Lines"
    )
    scanned_barcodes = fields.One2many(
        "quant.barcode.temp.line", "wizard_id", string="Temporary Scanned Barcodes"
    )

    @api.onchange("barcode")
    def _onchange_barcode(self):
        if not self.barcode:
            return

        # Parsitaan ja tallennetaan viivakoodin GS1-osat
        parsed = parse_gs1_barcode(self.barcode)

        # Lisää uusi rivi väliaikaisiin
        self.write(
            {
                "scanned_barcodes": [
                    (
                        0,
                        0,
                        {
                            "barcode": self.barcode,
                            "ai_01": parsed.get("01"),
                            "ai_10": parsed.get("10"),
                            "ai_17": parsed.get("17"),
                        },
                    )
                ]
            }
        )

        # Tyhjennä kenttä seuraavaa skannausta varten
        self.barcode = ""

        # Kokoa kaikki aiemmin skannatut GS1-data
        all_gs1_data = {}
        for line in self.scanned_barcodes:
            gs1 = parse_gs1_barcode(line.barcode)
            all_gs1_data.update(gs1)

        product_code = all_gs1_data.get("01")
        lot_name = all_gs1_data.get("10")
        expiration_raw = all_gs1_data.get("17")

        # Viestin muodostus
        missing = []
        if not product_code:
            missing.append("(01) product code")
        if not lot_name:
            missing.append("(10) lot number")

        if missing:
            self.info_message = _("Waiting for: ") + ", ".join(missing)
            return
        else:
            self.info_message = ""

        # Käsitellään eräpäivä
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
            available_lots = Lot.search([("product_id", "=", product.id)]).mapped(
                "name"
            )

            if available_lots:
                lot_list_str = ", ".join(available_lots)
                raise UserError(
                    _(
                        "Product '%(product)s' was found in stock,"
                        " but no lot with name '%(lot)s' exists.\n\n"
                        "Available lots for this product: %(lots)s"
                    )
                    % {
                        "product": product.display_name,
                        "lot": lot_name,
                        "lots": lot_list_str,
                    }
                )
            else:
                raise UserError(
                    _(
                        "Product '%(product)s' was found in stock,"
                        " but no lots exist in the system."
                    )
                    % {"product": product.display_name}
                )

        quant = Quant.search(
            [("product_id", "=", product.id), ("lot_id", "=", lot.id)], limit=1
        )

        if not quant:
            raise UserError(
                _("No stock found for product '%(product)s'.")
                % {"product": product.display_name}
            )

        already = self.scanned_line_ids.filtered(
            lambda li: li.product_id == product and li.lot_id == lot
        )
        if already:
            raise UserError(
                _("Lot '%(lot)s' for product '%(product)s' already scanned.")
                % {"lot": lot.name, "product": product.display_name}
            )

        # Lisää uusi rivi
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

        # Tyhjennetään väliaikaiset
        self.scanned_barcodes = [(5, 0, 0)]

    def action_apply(self):
        self.ensure_one()
        if not self.scanned_line_ids:
            raise UserError(
                _(
                    "No scanned lines to apply."
                    " Please scan at least one product before saving."
                )
            )
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
                    % {"product": line.product_id.display_name, "lot": line.lot_id.name}
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


class QuantBarcodeTempLine(models.TransientModel):
    _name = "quant.barcode.temp.line"
    _description = "Temporary Scanned Barcode"

    wizard_id = fields.Many2one("quant.barcode.update.wizard", ondelete="cascade")
    barcode = fields.Char(required=True)
    ai_01 = fields.Char(string="GTIN (01)")
    ai_10 = fields.Char(string="Lot (10)")
    ai_17 = fields.Char(string="Expiry (17)")
