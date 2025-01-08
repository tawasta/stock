from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_aggregated_product_quantities(self, **kwargs):
        aggregated_move_lines = super()._get_aggregated_product_quantities(**kwargs)

        for aggregated_move_line in aggregated_move_lines:
            quantity = aggregated_move_lines[aggregated_move_line].get("quantity", 0)
            product = aggregated_move_lines[aggregated_move_line].get("product", False)

            if product and quantity:
                weight = quantity * product.weight
                aggregated_move_lines[aggregated_move_line]["weight"] = weight

        return aggregated_move_lines
