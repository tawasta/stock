import logging
import re
from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


def parse_gs1_barcode(barcode_str):
    pattern = r"\((\d{2})\)([^\(]+)"
    matches = re.findall(pattern, barcode_str)

    data = {}
    for ai, value in matches:
        data[ai] = value.strip()
    return data


class StockReceiptWizard(models.TransientModel):
    _name = "stock.receipt.wizard"
    _description = "Stock Receipt Wizard"

    barcode_input = fields.Char(string="Scan Barcode")
    line_ids = fields.One2many("stock.receipt.wizard.line", "wizard_id", string="Lines")

    lot_ids = fields.Many2many("stock.receipt.lot", string="Lots")

    @api.onchange("barcode_input")
    def _onchange_barcode_input(self):
        if not self.barcode_input:
            return

        gs1_data = parse_gs1_barcode(self.barcode_input)

        product_code = gs1_data.get("01")
        expiration_raw = gs1_data.get("17")
        lot_name = gs1_data.get("10")

        if not product_code:
            return {
                "warning": {
                    "title": _("Barcode error"),
                    "message": _("Barcode missing (01) product code."),
                }
            }

        product = self.env["product.product"].search(
            [
                "|",
                ("barcode", "=", product_code),
                ("default_code", "=", product_code),
            ],
            limit=1,
        )
        if not product:
            return {
                "warning": {
                    "title": _("Product not found"),
                    "message": _("No product found with barcode '%s'.")
                    % self.barcode_input,
                }
            }

        move = self.env["stock.move"].search(
            [("product_id", "=", product.id), ("state", "=", "assigned")],
            order="date asc",
            limit=1,
        )
        if not move:
            return {
                "warning": {
                    "title": _("Stock move not found"),
                    "message": _("No stock move found for product '%s'.")
                    % product.name,
                }
            }

        existing_line = self.line_ids.filtered(
            lambda li: li.stock_move_id.id == move.id
        )
        if existing_line:
            existing_line.quantity += 1.0

            expiration_date = None
            if expiration_raw and re.match(r"\d{6}", expiration_raw):
                try:
                    expiration_date = datetime.strptime(expiration_raw, "%y%m%d").date()
                except ValueError as err:
                    raise UserError(
                        _("The expiration date in the barcode is invalid.")
                    ) from err

            self.lot_ids |= self.env["stock.receipt.lot"].create(
                {
                    "product_id": product.id,
                    "stock_move_id": move.id,
                    "lot_name": lot_name,
                    "expiration_date": expiration_date,
                }
            )

        else:
            self.line_ids |= self.env["stock.receipt.wizard.line"].new(
                {
                    "product_id": product.id,
                    "barcode": self.barcode_input,
                    "quantity": 1.0,
                    "stock_move_id": move.id,
                }
            )

            expiration_date = None
            if expiration_raw and re.match(r"\d{6}", expiration_raw):
                try:
                    expiration_date = datetime.strptime(expiration_raw, "%y%m%d").date()
                except ValueError as err:
                    raise UserError(
                        _("The expiration date in the barcode is invalid.")
                    ) from err

            self.lot_ids |= self.env["stock.receipt.lot"].create(
                {
                    "product_id": product.id,
                    "stock_move_id": move.id,
                    "lot_name": lot_name,
                    "expiration_date": expiration_date,
                }
            )
        self.barcode_input = False

    def validate_receipt_lines(self):
        # TODO: Lisää validointisäännöt tänne tarvittaessa
        pass

    def post_process_receipt_line(self, receipt_line):
        # TODO: Lisää myöhemmin riveihin liittyvä lisälogiikka tänne
        pass

    def action_confirm(self):
        if not self.line_ids:
            raise UserError(
                _(
                    "No receipt lines to confirm."
                    " Please scan at least one product before confirming."
                )
            )
        receipt = self.env["stock.receipt"].create({"user_id": self.env.user.id})
        for line in self.line_ids:
            self.env["stock.receipt.line"].create(
                {
                    "receipt_id": receipt.id,
                    "product_id": line.product_id.id,
                    "barcode": line.barcode,
                    "quantity": line.quantity,
                    "stock_move_id": line.stock_move_id.id,
                }
            )

            for lot in self.lot_ids:
                new_lot = self.env["stock.lot"].create(
                    {
                        "name": lot.lot_name,
                        "product_id": lot.product_id.id,
                        "product_qty": 1,
                        "expiration_date": lot.expiration_date
                        if "expiration_date" in lot
                        else False,
                    }
                )
                move_line = self.env["stock.move.line"].search(
                    [
                        ("move_id", "=", line.stock_move_id.id),
                        ("product_id", "=", line.product_id.id),
                    ],
                    order="lot_id desc",
                    limit=1,
                )

                if move_line:
                    move_line.write(
                        {
                            "lot_id": new_lot.id,
                        }
                    )

        # Kirjaa chatteriin viesti vastaanotosta
        lines_info = "\n".join(
            [
                _("- %(product)s (Barcode: %(barcode)s), Quantity: %(qty).2f")
                % {
                    "product": line.product_id.display_name,
                    "barcode": line.barcode or _("N/A"),
                    "qty": line.quantity,
                }
                for line in self.line_ids
            ]
        )

        body = _(
            "Stock receipt confirmed by %(user)s.\n\nReceived lines:\n%(lines)s"
        ) % {
            "user": self.env.user.name,
            "lines": lines_info,
        }
        receipt.message_post(body=body, subtype_xmlid="mail.mt_comment")
        return {
            "type": "ir.actions.act_window",
            "res_model": "stock.receipt",
            "res_id": receipt.id,
            "view_mode": "form",
        }


class StockReceiptWizardLine(models.TransientModel):
    _name = "stock.receipt.wizard.line"
    _description = "Stock Receipt Wizard Line"

    wizard_id = fields.Many2one(
        "stock.receipt.wizard", required=True, ondelete="cascade"
    )
    product_id = fields.Many2one("product.product", required=True)
    barcode = fields.Char()
    quantity = fields.Float(default=1.0)
    stock_move_id = fields.Many2one("stock.move")


class StockReceiptLot(models.Model):
    _name = "stock.receipt.lot"
    _description = "Stock Receipt Lot"

    lot_name = fields.Char(
        string="Lot Number",
    )
    product_id = fields.Many2one("product.product", readonly=1)
    expiration_date = fields.Date()
    stock_move_id = fields.Many2one("stock.move", string="Stock Move", readonly=1)
