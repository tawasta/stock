
from odoo import api, models


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.model
    def create(self, vals):
        order_id = vals.get('order_id', False)
        if order_id:
            order = self.env['sale.order'].search([('id', '=', order_id)])
            if order.procurement_group_id:
                order.procurement_group_id.force_unreserve = True

        return super().create(vals)
