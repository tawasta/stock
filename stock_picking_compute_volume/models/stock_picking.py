from odoo import fields, models

from odoo.addons import decimal_precision as dp


class StockPicking(models.Model):

    _inherit = "stock.picking"

    total_compute_volume = fields.Float(
        string="Total Volume",
        digits_compute=dp.get_precision("Stock Weight"),
        compute=lambda self: self._compute_calculate_volume(),
    )

    volume_uom_name = fields.Char(related="move_lines.product_id.volume_uom_name")

    def _compute_calculate_volume(self):
        """Calculate the total volume for the whole
        picking by summing the line volumes"""

        total = 0.0
        for line in self.move_lines:
            total += line.product_id.volume * line.product_uom_qty

        self.total_compute_volume = total
