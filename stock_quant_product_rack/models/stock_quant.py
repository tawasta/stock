from odoo import fields, models


class StockQuant(models.Model):

    _inherit = "stock.quant"

    product_template_loc_rack = fields.Char(
        related="product_id.product_tmpl_id.loc_rack"
    )
