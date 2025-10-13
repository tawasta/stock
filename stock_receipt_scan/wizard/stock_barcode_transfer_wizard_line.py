from odoo import fields, models


class StockBarcodeTransferWizardLine(models.TransientModel):
    _name = "stock.barcode.transfer.wizard.line"
    _description = "Barcode transfer wizard line"

    wizard_id = fields.Many2one(
        "stock.barcode.transfer.wizard", required=True, ondelete="cascade"
    )
    product_id = fields.Many2one("product.product", required=True, readonly=True)
    lot_id = fields.Many2one("stock.lot", readonly=True)
    quant_id = fields.Many2one("stock.quant", readonly=True)
    quantity = fields.Float(default=1.0)
    expiration_date = fields.Date(readonly=True)
    location_src_id = fields.Many2one(
        "stock.location",
        string="Source Location",
        domain=[("usage", "=", "internal")],
        readonly=True,
    )
    stock_move_id = fields.Many2one("stock.move", readonly=True)
