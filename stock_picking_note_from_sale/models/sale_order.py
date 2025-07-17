from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super().action_confirm()

        for pick in self.picking_ids:
            if not pick.note:
                pick.write({"note": self.note or ""})

        return res
