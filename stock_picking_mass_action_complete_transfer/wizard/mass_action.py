from odoo import models


class StockPickingMassAction(models.TransientModel):

    _inherit = "stock.picking.mass.action"

    def mass_action(self):
        res = super().mass_action()
        if res and res.get("res_model") == "stock.backorder.confirmation":
            picks = res.get("context") and res.get("context").get("active_ids")
            if picks:
                picks = self.env["stock.picking"].search([("id", "in", picks)])
                return picks.action_generate_backorder_wizard()
        return res
