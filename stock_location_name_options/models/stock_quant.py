from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    location_id_short_name = fields.Char(
        related="location_id.name",
        string="Location (Short)",
        readonly=True,
        store=False,
    )
