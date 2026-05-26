from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    use_default_location = fields.Boolean(copy=False, store=True, default=False)
