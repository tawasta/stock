from odoo import api, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    @api.onchange("picking_type_id", "partner_id")
    def onchange_picking_type(self):
        super().onchange_picking_type()
        # We do not return a possible warning
        return
