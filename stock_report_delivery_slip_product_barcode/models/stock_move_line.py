import logging

from odoo import models

_logger = logging.getLogger(__name__)


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_aggregated_product_quantities(self, **kwargs):
        """
        Store also products' barcodes in the aggregated dict so they're available in the
        delivery slip print
        """

        aggregated_move_lines = super()._get_aggregated_product_quantities(**kwargs)
        for aggregated_move_line in aggregated_move_lines:
            barcode = aggregated_move_lines[aggregated_move_line]["product"].barcode
            aggregated_move_lines[aggregated_move_line]["barcode"] = barcode

        return aggregated_move_lines
