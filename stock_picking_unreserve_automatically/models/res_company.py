from odoo import fields, models


class ResCompany(models.Model):

    _inherit = "res.company"

    force_unreserve = fields.Boolean(
        string="Force unreserve",
    )
