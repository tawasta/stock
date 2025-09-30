from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    use_source_color = fields.Boolean(related="location_id.use_source_color")
    use_destination_color = fields.Boolean(
        related="location_dest_id.use_destination_color"
    )
