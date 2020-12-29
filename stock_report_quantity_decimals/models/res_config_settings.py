from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    stock_report_decimal_precision = fields.Integer(
        related='company_id.stock_report_decimal_precision',
        readonly=False,
    )
