from odoo import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    is_excess_location = fields.Boolean("Is an Excess Location")
