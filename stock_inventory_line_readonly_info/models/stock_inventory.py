from odoo import _, fields, models


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    count_inventory_lines = fields.Integer(
        compute=lambda self: self._compute_count_inventory_lines()
    )

    line_ids = fields.One2many(
        "stock.inventory.line",
        "inventory_id",
        string="Inventories",
        copy=False,
        readonly=False,
        states={"done": [("readonly", True)]},
    )

    def _compute_count_inventory_lines(self):
        for inventory in self:
            if inventory.line_ids:
                inventory.count_inventory_lines = len(inventory.line_ids.ids)
            else:
                inventory.count_inventory_lines = 0

    def action_validated_inventory_lines(self):
        self.ensure_one()
        action = {
            "type": "ir.actions.act_window",
            "views": [
                (
                    self.env.ref(
                        "stock_inventory_line_readonly_info.stock_inventory_line_tree"
                    ).id,
                    "tree",
                )
            ],
            "view_mode": "tree",
            "name": _("Inventory Lines"),
            "res_model": "stock.inventory.line",
        }
        domain = [
            ("inventory_id", "=", self.id),
            ("location_id.usage", "in", ["internal", "transit"]),
        ]
        action["domain"] = domain
        return action
