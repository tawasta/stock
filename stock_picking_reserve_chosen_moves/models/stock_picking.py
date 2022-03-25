
from odoo import api, models


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    @api.multi
    def do_unreserve(self):
        for picking in self:
            for move in picking.move_lines:
                move.move_has_been_reserved = False
        super().do_unreserve()

    @api.multi
    def action_assign(self):
        res = super().action_assign()
        moves = self.mapped('move_lines').filtered(
                lambda move: move.state not in ('draft', 'cancel', 'done'))
        for move in moves:
            if move.product_uom_qty == move.reserved_availability:
                move.move_has_been_reserved = True
        return res
