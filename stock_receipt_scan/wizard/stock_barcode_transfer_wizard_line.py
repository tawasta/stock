from odoo import fields, models


class StockBarcodeTransferWizardLine(models.TransientModel):
    _name = "stock.barcode.transfer.wizard.line"
    _description = "Barcode transfer wizard line"

    wizard_id = fields.Many2one(
        "stock.barcode.transfer.wizard", required=True, ondelete="cascade"
    )
    product_id = fields.Many2one("product.product", required=True)
    lot_id = fields.Many2one("stock.lot", readonly=True)
    lot_name = fields.Char(readonly=True)
    quantity = fields.Float(default=1.0)
    expiration_date = fields.Date(readonly=True)
    location_id = fields.Many2one(
        "stock.location", required=True, domain=[("usage", "=", "internal")]
    )
