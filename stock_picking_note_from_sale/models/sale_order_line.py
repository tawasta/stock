# -*- coding: utf-8 -*-
from odoo import models, api


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.multi
    def _action_procurement_create(self):
        procurements = super(SaleOrderLine, self). \
            _action_procurement_create()

        StockPicking = self.env['stock.picking']
        for procurement in procurements:
            # Search all pickings in this procurement
            pickings = StockPicking.search([(
                ('group_id', '=', procurement.group_id.id)
            )])

            for picking in pickings:

                if not picking.note:
                    picking.note = self[0].order_id.note

        return procurements
