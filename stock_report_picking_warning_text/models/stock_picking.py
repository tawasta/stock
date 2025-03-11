from odoo import api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.onchange("picking_type_id", "partner_id")
    def _onchange_picking_type(self):
        res = super()._onchange_picking_type()

        if res and res.get("warning"):
            # We do not return a possible warning
            return {}
        else:
            return res
