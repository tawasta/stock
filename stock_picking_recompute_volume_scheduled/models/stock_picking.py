import logging

from odoo import _, models

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _cron_recompute_volume(self, batch):
        pickings = self.env["stock.picking"].search([("id", "in", batch)])
        for picking in pickings:
            picking._compute_volume()
        return batch, "Success"

    def cron_recompute_volume(self):
        """Recomputes volume for each stock picking"""

        pickings = self.env["stock.picking"].search([]).ids

        batch_pickings = list()
        interval = 50

        for x in range(0, len(pickings), interval):
            batch_pickings.append(pickings[x : x + interval])

        for batch in batch_pickings:
            job_desc = _("Recompute volume for stock pickings: {}").format(batch)

            self.with_delay(description=job_desc)._cron_recompute_volume(batch)

        _logger.info("Recomputing volume completed")
