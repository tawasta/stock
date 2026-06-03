from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    delivery_report_ordered_term = fields.Char(
        related="company_id.delivery_report_ordered_term",
        readonly=False,
    )
    delivery_report_delivered_term = fields.Char(
        related="company_id.delivery_report_delivered_term",
        readonly=False,
    )
