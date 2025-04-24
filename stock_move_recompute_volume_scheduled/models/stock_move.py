import logging

from odoo import _, models

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move"

    def _cron_recompute_volume(self, batch):
        moves = self.env["stock.move"].search([("id", "in", batch)])
        for move in moves:
            move._compute_volume()
        return batch, "Success"

    def cron_recompute_volume(self):
        """Recomputes volume for each stock move"""

        moves = self.env["stock.move"].search([]).ids

        batch_moves = list()
        interval = 50

        for x in range(0, len(moves), interval):
            batch_moves.append(moves[x : x + interval])

        for batch in batch_moves:
            job_desc = _("Recompute volume for stock moves: {}").format(batch)

            self.with_delay(description=job_desc)._cron_recompute_volume(batch)

        _logger.info("Recomputing volume completed")
