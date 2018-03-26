# -*- coding: utf-8 -*-
from odoo import models, api, _, exceptions


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def deliver(self):
        # Deliver the SO directly without going to the picking view.
        # Force stock availability if necessary.

        self.ensure_one()
        self.action_confirm()

        incomplete_pickings = \
            [x for x in self.picking_ids if x.state not in ['cancel', 'done']]

        if len(incomplete_pickings) == 0:
            msg = _('{} does not have a pending delivery order, '
                    'please deliver the sale order manually.'.format(self.name))
            raise exceptions.ValidationError(msg)

        elif len(incomplete_pickings) > 1:
            # If for some reason the SO has multiple open delivery orders,
            # raise an exception.
            # This is because the autodelivery function utilizes
            # the delivery wizard, which expects only a single delivery order.
            msg = _('You can autodeliver a sale order only if it has a single '
                    'delivery order waiting, but {} has multiple. Please '
                    'deliver the sale order manually'.format(self.name))
            raise exceptions.ValidationError(msg)

        else:
            incomplete_pickings[0].force_assign()

            # res contains info for launching the delivery wizard.
            # Use this to get the wizard ID and model to call wizard's
            # process method manually
            res = incomplete_pickings[0].do_new_transfer()

            if res['res_model'] != 'stock.immediate.transfer':
                # In case Odoo for some reason returned
                # stock.backorder.confirmation wizard in
                # do_new_transfer() instead
                raise exceptions.except_orm(
                    'Error',
                    'Immediate transfer not possible, '
                    'please deliver the sale order manually')
            else:
                self.env['stock.immediate.transfer'].browse(
                    res['res_id']
                ).process()
