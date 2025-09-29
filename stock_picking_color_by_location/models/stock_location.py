from odoo import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    use_destination_color = fields.Boolean(
        string="Use Destination color in tree view", copy=False
    )
    use_source_color = fields.Boolean(
        string="Use Source location color in tree view", copy=False
    )
