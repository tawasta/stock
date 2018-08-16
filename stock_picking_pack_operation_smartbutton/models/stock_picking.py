# -*- coding: utf-8 -*-
from odoo import models, api


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    @api.multi
    def action_view_pack_operations(self):
        pack_ops = self.mapped('pack_operation_ids')
        action = self.env.ref(
            ('stock_picking_pack_operation_smartbutton.'
             'stock_pack_operation_action')
        ).read()[0]

        action['domain'] = [('id', 'in', pack_ops.ids)]

        return action
