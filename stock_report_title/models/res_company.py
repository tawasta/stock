from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    delivery_slip_title = fields.Char(
        string="Delivery slip title",
        default="",
        translate=True,
    )
    hide_delivery_slip_title = fields.Boolean(
        string="Hide delivery slip title",
        default=False,
    )
    hide_delivery_slip_text = fields.Boolean(
        string="Hide delivery slip text",
        default=True,
    )
    hide_delivery_slip_report_name = fields.Boolean(
        string="Hide delivery slip report name",
        default=False,
    )
    hide_picking_name = fields.Boolean(
        string="Hide picking name",
        default=False,
    )
