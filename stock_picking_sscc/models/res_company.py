from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    sscc_extension_digit = fields.Integer(
        string="Extension Digit for SSCC",
        default=1,
    )

    sscc_company_prefix = fields.Char(
        string="Company Prefix for SSCC",
        default=23456789,
    )
