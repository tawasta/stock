import logging

from odoo import _, models

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move"

    def _cron_recompute_state(self, batch):
        moves = self.env["stock.move"].search([("id", "in", batch)])
        for move in moves:
            move._recompute_state()
        return batch, "Success"

    def cron_recompute_state(self):
        """Recomputes status for each stock move"""

        moves = self.env["stock.move"].search([]).ids

        batch_moves = list()
        interval = 50

        for x in range(0, len(moves), interval):
            batch_moves.append(moves[x : x + interval])

        for batch in batch_moves:
            job_desc = _("Recompute status for stock moves: {}").format(batch)

            self.with_delay(description=job_desc)._cron_recompute_state(batch)

        _logger.info("Recomputing status completed")
