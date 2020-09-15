
from odoo import fields, models


class ProductProduct(models.Model):

    _inherit = 'product.product'

    stock_value = fields.Float(store=True)
    qty_at_date = fields.Float(store=True)
