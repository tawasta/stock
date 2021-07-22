# -*- coding: utf-8 -*-
from odoo import fields, models


class StockPickingSaleOrderWarning(models.TransientModel):

    _name = 'stock.picking.sale.order.warning'

    text = fields.Char(string="Text", readonly=True)
    picking_id = fields.Many2one("stock.picking")

    def validate(self):
        pick = self.env['stock.picking'].search([('id','=',self.picking_id.id)])
        return pick.do_new_transfer()
