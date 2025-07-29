from odoo import models


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    def action_state_to_in_progress(self):
        self.ensure_one()

        quants = self._get_quants(self.location_ids)

        inventory_ids = self.env["stock.inventory"].search(
            [("state", "=", "in_progress")]
        )

        quants._check_no_duplicate_line(inventory_ids, quants)

        self.write(
            {
                "state": "in_progress",
                "stock_quant_ids": [(6, 0, quants.ids)],
            }
        )
        quants.write(
            {
                "to_do": True,
                "user_id": self.responsible_id,
                "inventory_date": self.date,
                "current_inventory_id": self.id,
            }
        )
        return
