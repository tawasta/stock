from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def set_moves_to_done(self):
        for move in self.move_ids.filtered(lambda m: m.state not in ["done", "cancel"]):
            move.quantity = move.product_uom_qty
