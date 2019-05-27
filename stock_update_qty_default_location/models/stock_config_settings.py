from odoo import fields, models


class StockConfigSettings(models.TransientModel):

    _inherit = 'stock.config.settings'

    default_stock_update_qty_location = fields.Many2one(
        related='company_id.default_stock_update_qty_location'
    )
