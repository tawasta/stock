from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    product_tag_ids = fields.Many2many(related="product_tmpl_id.product_tag_ids")
