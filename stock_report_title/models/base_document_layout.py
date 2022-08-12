from odoo import fields, models


class BaseDocumentLayoutInherit(models.TransientModel):
    _inherit = "base.document.layout"

    show_delivery_slip_report_name = fields.Boolean(
        related="company_id.show_delivery_slip_report_name", readonly=True
    )
