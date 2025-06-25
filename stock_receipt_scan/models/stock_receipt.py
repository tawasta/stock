from odoo import fields, models


class StockReceipt(models.Model):
    _name = "stock.receipt"
    _description = "Stock Receipt"
    _inherit = ["mail.thread"]

    user_id = fields.Many2one(
        "res.users", string="User", default=lambda self: self.env.user, readonly=True
    )
    create_date = fields.Datetime(string="Date", readonly=True)
    line_ids = fields.One2many("stock.receipt.line", "receipt_id", string="Lines")


class StockReceiptLine(models.Model):
    _name = "stock.receipt.line"
    _description = "Stock Receipt Line"

    receipt_id = fields.Many2one("stock.receipt", required=True, ondelete="cascade")
    product_id = fields.Many2one("product.product", string="Product", required=True)
    barcode = fields.Char()
    quantity = fields.Float(default=1.0)
    stock_move_id = fields.Many2one("stock.move", readonly=True)
    stock_picking_id = fields.Many2one(
        related="stock_move_id.picking_id", readonly=True
    )
