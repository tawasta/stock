from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    location_id_short_name = fields.Char(
        related="location_id.name",
        string="From (Short)",
        readonly=True,
        store=False,
    )
    location_dest_id_short_name = fields.Char(
        related="location_dest_id.name",
        string="To (Short)",
        readonly=True,
        store=False,
    )
