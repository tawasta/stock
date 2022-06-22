from odoo import api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.depends("order_line")
    def _compute_delivery_state(self):
        for order in self:
            order.delivery_set = False
