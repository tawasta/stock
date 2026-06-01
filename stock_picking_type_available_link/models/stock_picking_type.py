from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_products_available = fields.Boolean(
        string="Products Available",
        compute="_compute_is_products_available",
        search="_search_is_products_available",
    )

    def _compute_is_products_available(self):
        for picking in self:
            picking.is_products_available = (
                picking._is_products_available_for_dashboard()
            )

    def _is_products_available_for_dashboard(self):
        self.ensure_one()
        return (
            self.picking_type_code == "outgoing"
            and self.state == "assigned"
            and self.products_availability_state == "available"
        )

    def _search_is_products_available(self, operator, value):
        if operator not in ("=", "!="):
            return [("id", "=", 0)]

        candidates = self.search(
            [
                ("picking_type_code", "=", "outgoing"),
                ("state", "=", "assigned"),
            ]
        )

        available_ids = candidates.filtered(
            lambda picking: picking._is_products_available_for_dashboard()
        ).ids

        positive = (operator == "=" and bool(value)) or (
            operator == "!=" and not bool(value)
        )

        if positive:
            return [("id", "in", available_ids)]

        return [("id", "not in", available_ids)]


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    count_picking_available = fields.Integer(
        string="Available",
        compute="_compute_count_picking_available",
    )

    def _get_picking_available_domain(self):
        self.ensure_one()
        return [
            ("picking_type_id", "=", self.id),
            ("is_products_available", "=", True),
        ]

    def _compute_count_picking_available(self):
        Picking = self.env["stock.picking"]

        for picking_type in self:
            if picking_type.code != "outgoing":
                picking_type.count_picking_available = 0
                continue

            picking_type.count_picking_available = Picking.search_count(
                picking_type._get_picking_available_domain()
            )

    def get_action_picking_tree_available(self):
        self.ensure_one()
        action = self._get_action("stock.stock_picking_action_picking_type")
        action["domain"] = self._get_picking_available_domain()
        return action
