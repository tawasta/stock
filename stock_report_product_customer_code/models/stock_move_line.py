from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_aggregated_product_quantities(self, **kwargs):
        aggregated_move_lines = super()._get_aggregated_product_quantities(**kwargs)
        for move_line in self:
            name = move_line.product_id.display_name
            description = move_line.move_id.description_picking
            if description == name or description == move_line.product_id.name:
                description = False
            uom = move_line.product_uom_id
            product = move_line.product_id
            move = move_line.move_id
            line_key = (
                f"{product.id}_{product.display_name}_"
                f'{description or ""}_{uom.id}_{move.product_packaging_id or ""}_'
            )
            customer_code = move_line.move_id.product_customer_code

            if not customer_code:
                customer_code = move_line.move_id.sale_line_id.product_customer_code

            if line_key in aggregated_move_lines:
                aggregated_move_lines[line_key]["customer_code"] = customer_code

        return aggregated_move_lines
