from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    show_delivery_slip_text = fields.Boolean(
        string="Show delivery slip header",
        related="company_id.show_delivery_slip_text",
        readonly=False,
    )
