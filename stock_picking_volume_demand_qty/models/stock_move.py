import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.depends("product_id", "product_uom_qty", "state", "quantity")
    def _compute_volume(self):
        for move in self:
            qty = move.product_uom_qty

            if not move.product_id:
                new_volume = 0.0
            else:
                new_volume = move.product_id._get_volume_for_qty(
                    qty,
                    move.product_uom,
                )

            move.volume = new_volume