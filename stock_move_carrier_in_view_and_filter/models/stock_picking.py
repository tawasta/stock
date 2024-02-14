from odoo import models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    def write(self, vals):
        res = super().write(vals)

        carrier_id = vals.get("carrier_id", False)
        carrier_id = self.env["delivery.carrier"].browse(carrier_id)

        for move in self.move_lines:
            move.carrier_id = carrier_id

        return res
