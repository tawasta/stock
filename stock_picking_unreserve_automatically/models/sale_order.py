
from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    def _default_force_unreserve(self):
        return self.env.user.company_id.force_unreserve

    force_unreserve = fields.Boolean(copy=False,
        default=lambda self: self._default_force_unreserve())

    @api.multi
    def action_cancel(self):
        """ In case a sale order is canceled and confirmed again, it is
            necessary to set a procurement group's force_unreserve-field
            to True. This way the sale order's new transfer will not be
            reserved. """
        for order in self:
            if order.procurement_group_id:
                order.procurement_group_id.force_unreserve = True
            return super(SaleOrder, order).action_cancel()
