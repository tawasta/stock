from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    force_unreserve = fields.Boolean(
        string="Force Unreserve",
        related="company_id.force_unreserve",
        readonly=False,
    )
