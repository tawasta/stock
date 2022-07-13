from odoo import models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    def do_unreserve(self):
        """Mark all moves as not been reserved."""
        for picking in self:
            for move in picking.move_lines:
                move.move_has_been_reserved = False
        super().do_unreserve()

    def action_assign(self):
        """Mark all moves as reserved, which hides Reserve-button."""
        res = super().action_assign()
        moves = self.mapped("move_lines").filtered(
            lambda move: move.state not in ("draft", "cancel", "done")
        )
        for move in moves:
            if move.product_uom_qty == move.reserved_availability:
                move.move_has_been_reserved = True
        return res
