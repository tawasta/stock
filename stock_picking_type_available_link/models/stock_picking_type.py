from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    count_picking_available = fields.Integer(
        string="Available",
        compute="_compute_count_picking_available",
    )

    def _get_available_picking_domain(self):
        self.ensure_one()
        return [
            ("picking_type_id", "=", self.id),
            ("picking_type_code", "=", "outgoing"),
            ("state", "in", ["confirmed", "waiting", "assigned"]),
            ("products_availability_state", "=", "available"),
        ]

    def _compute_count_picking_available(self):
        for picking_type in self:
            if picking_type.code != "outgoing":
                picking_type.count_picking_available = 0
                continue

            picking_type.count_picking_available = self.env[
                "stock.picking"
            ].search_count(picking_type._get_available_picking_domain())

    def get_action_picking_tree_available(self):
        self.ensure_one()

        action = self.env["ir.actions.actions"]._for_xml_id(
            "stock.stock_picking_action_picking_type"
        )
        action["display_name"] = self.display_name
        action["domain"] = self._get_available_picking_domain()
        action["context"] = {
            "contact_display": "partner_address",
            "default_picking_type_id": self.id,
            "default_company_id": self.company_id.id,
        }
        return action
