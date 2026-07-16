from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    location_id_short_name = fields.Char(
        related="location_id.name",
        string="Source Location (Short)",
        readonly=True,
        store=False,
    )
    location_dest_id_short_name = fields.Char(
        related="location_dest_id.name",
        string="Destination Location (Short)",
        readonly=True,
        store=False,
    )
