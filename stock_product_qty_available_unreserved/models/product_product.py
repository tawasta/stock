from odoo import models, fields
from odoo.addons import decimal_precision as dp


class ProductProduct(models.Model):

    _inherit = 'product.product'

    qty_available_unreserved = fields.Float(
        string='Unreserved quantity on hand',
        compute='_compute_quantities',
        search='_search_qty_available_unreserved',
        digits=dp.get_precision('Product Unit of Measure'))

    def _compute_quantities(self):
        super(ProductProduct, self)._compute_quantities()

        for product in self:
            unreserved = product.qty_available - product.outgoing_qty
            product.qty_available_unreserved = unreserved
