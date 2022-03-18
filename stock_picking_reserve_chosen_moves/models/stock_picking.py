
from odoo import api, models


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    @api.multi
    def action_assign(self):
        # Modified Odoo's stock module's action_assign function. Checks if
        # some moves have reserve_this_move field ticked.
        if any([move for move in self.move_lines if move.reserve_this_move]) \
                and False in [move.reserve_this_move for move in self.move_lines]:
            moves = self.mapped('move_lines').filtered(
                lambda move: move.state not in ('draft', 'cancel', 'done')
            ).filtered(lambda move: move.reserve_this_move)

            if not moves:
                raise UserError(_('Nothing to check the availability for.'))
            moves._action_assign()
            return True
        # Do nothing if no reserve_this_move-field is ticked.
        elif not any([move.reserve_this_move for move in self.move_lines]):
            return True
        # Else clause just in case.
        else:
            super(StockPicking, self).action_assign()
