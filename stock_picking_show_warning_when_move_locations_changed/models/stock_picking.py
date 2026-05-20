from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    has_custom_line_locations = fields.Boolean(
        compute="_compute_has_custom_line_locations",
        help="Do any of the picking's moves have a source or destination location "
        "that differs from the picking's location.",
    )

    @api.depends(
        "move_ids.location_id",
        "move_ids.location_dest_id",
        "location_id",
        "location_dest_id",
        "state",
    )
    def _compute_has_custom_line_locations(self):
        for picking in self:
            picking.has_custom_line_locations = any(
                move.location_id != picking.location_id
                or move.location_dest_id != picking.location_dest_id
                for move in picking.move_ids
            )
