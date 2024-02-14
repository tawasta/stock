import logging
from functools import partial
from itertools import cycle, groupby
from operator import itemgetter

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class StockMove(models.Model):

    _inherit = "stock.move"

    carrier_id = fields.Many2one("delivery.carrier", store=True)

    @api.model
    def create(self, vals):
        picking_id = vals.get("picking_id", False)
        picking_id = self.env["stock.picking"].browse(picking_id)

        if picking_id:
            vals["carrier_id"] = picking_id.carrier_id.id or False

        return super().create(vals)

    @api.onchange("picking_id")
    def onchange_stock_picking_carrier(self):
        self.carrier_id = self.picking_id.carrier_id

    def picking_with_carrier(self):
        moves = self.env["stock.move"].search([]).sorted(key=lambda m: m.id)
        for move in moves:
            if move.picking_id.carrier_id:
                yield move

    def _cron_compute_stock_move_carrier(self, moves):
        for move in moves:
            move.carrier_id = move.picking_id.carrier_id
        return moves, "Success"

    def cron_compute_stock_move_carrier(self):
        """Computes all Stock Move carrier_id values"""

        def move_chunks(iterable, size=50):
            c = cycle((False,) * size + (True,) * size)
            return map(itemgetter(1), groupby(iterable, partial(next, c)))

        moves = self.picking_with_carrier()
        batch_moves = move_chunks(moves)

        for batch in batch_moves:
            job_desc = "Assign Carrier to moves"
            self.with_delay(description=job_desc)._cron_compute_stock_move_carrier(
                list(batch)
            )

        _logger.info("Cron compute Stock move Carrier completed")
