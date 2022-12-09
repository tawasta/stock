
from odoo import fields, models


class ProductProduct(models.Model):

    _inherit = 'product.product'

    value_location = fields.Float(string="Location value", compute="_compute_value_by_location")

    def _compute_value_by_location(self):
        """Computes values by location"""
        for product in self:
            domain_quant_loc, domain_move_in_loc, domain_move_out_loc = product._get_domain_locations()

            domain_quant_loc += [('product_id', '=', product.id)]
            quants = self.env['stock.quant'].search(domain_quant_loc)
            value_sum = sum([q.value for q in quants])

            product.value_location = value_sum
