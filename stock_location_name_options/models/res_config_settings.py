from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    location_name_report_style = fields.Selection(
        related="company_id.location_name_report_style",
        readonly=False,
    )
