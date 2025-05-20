from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        res = super().button_validate()

        if res and isinstance(res, dict) and res.get("params", False):
            res["params"]["anotherAction"] = {
                "type": "ir.actions.client",
                "tag": "soft_reload",
            }

        return res
