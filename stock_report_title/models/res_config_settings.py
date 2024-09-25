from odoo import fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    delivery_slip_title = fields.Char(
        string="Delivery slip title",
        related="company_id.delivery_slip_title",
        readonly=False,
        translate=True,
    )
    hide_delivery_slip_title = fields.Boolean(
        string="Hide delivery slip title",
        related="company_id.hide_delivery_slip_title",
        readonly=False,
    )
    hide_delivery_slip_report_name = fields.Boolean(
        string="Hide delivery slip report name",
        related="company_id.hide_delivery_slip_report_name",
        readonly=False,
    )
    hide_picking_title = fields.Boolean(
        string="Hide picking title",
        related="company_id.hide_picking_title",
        readonly=False,
    )
    hide_picking_report_name = fields.Boolean(
        string="Hide picking report name",
        related="company_id.hide_picking_report_name",
        readonly=False,
    )
