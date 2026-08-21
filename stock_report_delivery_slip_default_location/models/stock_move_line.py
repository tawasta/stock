from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_aggregated_product_quantities(self, **kwargs):
        """Store also the default location of a product in the aggregated dict for
        delivery slip print"""

        aggregated_move_lines = super()._get_aggregated_product_quantities(**kwargs)
        for aggregated_move_line in aggregated_move_lines:
            default_location_id = aggregated_move_lines[aggregated_move_line][
                "product"
            ].default_stock_move_location_id
            aggregated_move_lines[aggregated_move_line][
                "default_location"
            ] = default_location_id

        return aggregated_move_lines
