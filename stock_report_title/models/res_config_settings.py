from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    delivery_slip_title = fields.Char(
        string="Delivery slip title",
        related="company_id.delivery_slip_title",
        readonly=False,
        translate=True,
    )
    show_delivery_slip_text = fields.Boolean(
        string="Show delivery slip header",
        related="company_id.show_delivery_slip_text",
        readonly=False,
    )
    show_delivery_slip_report_name = fields.Boolean(
        string="Show delivery slip report name",
        related="company_id.show_delivery_slip_report_name",
        readonly=False,
    )
    show_picking_text = fields.Boolean(
        string="Show picking header",
        related="company_id.show_picking_text",
        readonly=False,
    )
    show_picking_report_name = fields.Boolean(
        string="Show picking report name",
        related="company_id.show_picking_report_name",
        readonly=False,
    )
