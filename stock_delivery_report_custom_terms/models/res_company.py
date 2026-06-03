from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    delivery_report_ordered_term = fields.Char(
        string="Delivery report: Ordered term",
        default="Ordered",
        translate=True,
    )
    delivery_report_delivered_term = fields.Char(
        string="Delivery report: Delivered term",
        default="Delivered",
        translate=True,
    )
