
from odoo import fields, models


class StockMove(models.Model):

    _inherit = 'stock.move'

    move_has_been_reserved = fields.Boolean(default=False)

    def reserve_this_move(self):
        self.move_has_been_reserved = True
        self._action_assign()
