from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    stock_update_qty_location_default = fields.Many2one(
        related='company_id.stock_update_qty_location_default',
        readonly=False,
    )
