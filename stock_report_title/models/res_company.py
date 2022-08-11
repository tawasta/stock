from odoo import fields, models


class ResCompany(models.Model):

    _inherit = "res.company"

    show_delivery_slip_text = fields.Boolean(
        string="Show delivery slip text",
    )
