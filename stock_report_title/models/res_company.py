from odoo import fields, models


class ResCompany(models.Model):

    _inherit = "res.company"

    delivery_slip_title = fields.Char(
        string="Delivery slip title",
        default="",
        translate=True,
    )
    show_delivery_slip_text = fields.Boolean(
        string="Show delivery slip text",
        default=True,
    )
    show_delivery_slip_report_name = fields.Boolean(
        string="Show delivery slip report name",
        default=True,
    )
    show_picking_text = fields.Boolean(
        string="Show picking text",
        default=True,
    )
    show_picking_report_name = fields.Boolean(
        string="Show picking report name",
        default=True,
    )
