from odoo import api, fields, models


class MrpProduction(models.Model):

    _inherit = 'mrp.production'

    created_from_stock_move = fields.One2many(
        comodel_name='stock.move', inverse_name='manufacturing_order_id')

    @api.multi
    def button_mark_done(self):
        res = super().button_mark_done()

        for stock in self.created_from_stock_move:
            stock.mo_to_complete = False

        return res
