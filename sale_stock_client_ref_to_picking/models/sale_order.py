from odoo import models, api


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        # Create pickings
        res = super(SaleOrder, self).action_confirm()

        # Write customer reference to pickings
        for record in self:
            picking_values = {
                'customer_reference': record.client_order_ref,
            }
            record.picking_ids.write(picking_values)

        return res
