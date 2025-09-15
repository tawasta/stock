
from odoo import fields, models


class StockRule(models.Model):

    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values):
        res = super()._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, company_id, values)

        dest_move = values.get('move_dest_ids', False)
        dest_move = dest_move and dest_move[0] or False

        if dest_move and not res.get('sale_line_id', False):
            res['sale_line_id'] = dest_move.sale_line_id.id

        return res
