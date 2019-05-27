from odoo import models, api


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        # Override the 'invoice_shipping_on_delivery' to always be False
        res = super(SaleOrder, self).action_confirm()
        for so in self:
            # invoice_shipping_on_delivery is always False
            so.invoice_shipping_on_delivery = False
        return res
