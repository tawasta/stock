from odoo import fields, models


class StockBarcodeTransferWizardTmpLine(models.TransientModel):
    # I don't think this model is needed anymore, but didn't remove it yet
    _name = "stock.barcode.transfer.wizard.tmp.line"
    _description = "Temporary Barcode transfer wizard line"

    wizard_id = fields.Many2one("stock.barcode.transfer.wizard", ondelete="cascade")
    barcode = fields.Char(required=True)
    # TODO: rename the fields to gtin, lot and expiry
    ai_01 = fields.Char(string="GTIN (01)")
    ai_10 = fields.Char(string="Lot (10)")
    ai_17 = fields.Char(string="Expiry (17)")
