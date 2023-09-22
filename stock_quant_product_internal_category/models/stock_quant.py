from odoo import fields, models


class StockQuant(models.Model):

    _inherit = "stock.quant"

    product_category = fields.Many2one(
        "product.category",
        related="product_id.categ_id",
    )
