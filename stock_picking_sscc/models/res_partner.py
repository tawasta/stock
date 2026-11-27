from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    use_sscc_code = fields.Boolean(string="Use SSCC code in picking", copy=False)
