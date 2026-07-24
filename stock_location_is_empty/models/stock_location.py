from odoo import _, fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    is_empty = fields.Boolean(
        "Is Empty", compute="_compute_is_empty", search="_search_is_empty"
    )

    def _compute_is_empty(self):
        groups = self.env["stock.quant"]._read_group(
            [
                ("location_id.usage", "in", ("internal", "transit")),
                ("location_id", "in", self.ids),
            ],
            ["location_id"],
            ["quantity:sum"],
        )
        groups = dict(groups)
        for location in self:
            location.is_empty = groups.get(location, 0) <= 0

    def _search_is_empty(self, operator, value):
        if operator not in ("=", "!=") or not isinstance(value, bool):
            raise NotImplementedError(
                _(
                    """The search does not support the %(operator)s
                    operator or %(value)s value."""
                ),
                operator=operator,
                value=value,
            )
        groups = self.env["stock.quant"]._read_group(
            [("location_id.usage", "in", ["internal", "transit"])],
            ["location_id"],
            ["quantity:sum"],
        )
        location_ids = {loc.id for loc, quantity in groups if quantity >= 0}
        if value and operator == "=" or not value and operator == "!=":
            return [("id", "not in", list(location_ids))]
        return [("id", "in", list(location_ids))]
