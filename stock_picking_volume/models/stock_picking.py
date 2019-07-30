# -*- coding: utf-8 -*-


from odoo import api, fields, models


class StockPicking(models.Model):

    _inherit = 'stock.pack.operation'

    volume = fields.Float(string='Volume', compute='_get_volume')

    @api.multi
    def _get_volume(self):
        for pack in self:
            pack.volume = pack.product_id.volume
