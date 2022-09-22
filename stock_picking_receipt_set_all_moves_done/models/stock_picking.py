from odoo import models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    def set_moves_to_done(self):
        # move_lines field's related model is stock.move
        for move in self.move_lines.filtered(
            lambda m: m.state not in ["done", "cancel"]
        ):
            for move_line in move.move_line_ids:
                move_line.qty_done = move_line.product_uom_qty
