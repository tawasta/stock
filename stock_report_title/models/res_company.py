from odoo import fields, models


class ResCompany(models.Model):

    _inherit = "res.company"

    show_delivery_slip_text = fields.Boolean(
        string="Show delivery slip text",
    )
    show_delivery_slip_report_name = fields.Boolean(
        string="Show delivery slip report name",
    )
