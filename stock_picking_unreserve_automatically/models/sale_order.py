
from odoo import fields, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    def _default_force_unreserve(self):
        return self.env.user.company_id.force_unreserve

    force_unreserve = fields.Boolean(copy=False,
        default=lambda self: self._default_force_unreserve())
