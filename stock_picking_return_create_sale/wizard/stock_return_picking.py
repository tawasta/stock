# -*- coding: utf-8 -*-
from odoo import models, api


class StockReturnPicking(models.TransientModel):

    _inherit = 'stock.return.picking'

    @api.multi
    def create_returns(self):
        res = super(StockReturnPicking, self).create_returns()

        picking_id = self.env['stock.picking'].browse(
            self.env.context.get('active_id'))

        if picking_id and picking_id.sale_id:
            # If the sale is already invoiced, create a new sale order
            if picking_id.sale_id.invoice_status == 'invoiced':
                refund_moves = self.product_return_moves.filtered(
                    'to_refund_so',
                )

                SaleOrder = self.env['sale.order']
                SaleOrderLine = self.env['sale.order.line']

                if refund_moves:
                    # Create a new sale order
                    sale_order = SaleOrder.create(dict(
                        partner_id=picking_id.sale_id.partner_id.id,
                    ))

                for move in refund_moves:
                    SaleOrderLine.create(dict(
                        order_id=sale_order.id,
                        product_id=move.product_id.id,
                        product_uom_qty=-move.quantity,
                    ))

        return res
