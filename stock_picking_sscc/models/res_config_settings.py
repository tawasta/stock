from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sscc_extension_digit = fields.Integer(
        string="Extension Digit for SSCC",
        related="company_id.sscc_extension_digit",
        help="Set a default extension digit for SSCC code used in stock pickings.",
        readonly=False,
    )

    sscc_company_prefix = fields.Char(
        string="Company Prefix for SSCC",
        related="company_id.sscc_company_prefix",
        help="Set a default company prefix for SSCC code used in stock pickings.",
        readonly=False,
    )
