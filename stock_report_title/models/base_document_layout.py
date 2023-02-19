from odoo import fields, models


class BaseDocumentLayoutInherit(models.TransientModel):
    _inherit = "base.document.layout"

    delivery_slip_title = fields.Char(
        related="company_id.delivery_slip_title",
        readonly=True,
    )
    show_delivery_slip_report_name = fields.Boolean(
        related="company_id.show_delivery_slip_report_name", readonly=True
    )
    show_picking_report_name = fields.Boolean(
        related="company_id.show_picking_report_name", readonly=True
    )
