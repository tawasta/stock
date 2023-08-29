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
            line_key = (
                str(move_line.product_id.id)
                + "_"
                + name
                + (description or "")
                + "uom "
                + str(uom.id)
            )
            sale_line_qty = move_line.move_id.sale_line_id.product_uom_qty
            if line_key in aggregated_move_lines:
                aggregated_move_lines[line_key]["sale_line_qty"] = sale_line_qty

        return aggregated_move_lines
