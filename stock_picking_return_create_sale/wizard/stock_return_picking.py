# -*- coding: utf-8 -*-
from odoo import models, api


class StockReturnPicking(models.TransientModel):

    _inherit = 'stock.return.picking'

    @api.multi
    def create_returns(self):
        res = super(StockReturnPicking, self).create_returns()

        res_id = res.get('res_id')
        if res_id:
            picking_id = self.env['stock.picking'].browse([res_id])

        if picking_id and picking_id.sale_id:
            # If the sale is already invoiced, create a new sale order
            if picking_id.sale_id.invoice_status == 'invoiced':
                # Create a new sale order
                pass

        return res
