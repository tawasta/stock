from odoo import api, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    @api.multi
    def action_packing_wizard(self):
        res = self.env["ir.actions.act_window"].for_xml_id(
            "stock_picking_quick_packing", "wizard_action"
        )

        return res
