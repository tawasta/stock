from odoo import fields, models


class StockMove(models.Model):

    _inherit = "stock.move"

    move_has_been_reserved = fields.Boolean(default=False)

    def reserve_this_move(self):
        """Mark this move as reserved."""
        self._action_assign()
        if self.state in ("assigned", "done"):
            self.move_has_been_reserved = True
