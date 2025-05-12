from odoo import fields, models

import logging

_logger = logging.getLogger(__name__)


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _is_stock_picking_report(self, report_ref):
        """Check if the stock picking report is being printed"""
        return (
            self._get_report(report_ref).report_name
            == "stock_report_enable_translation_by_partner.report_picking"
        )

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        """When printing picking, log the printing date"""
        if self._is_stock_picking_report(report_ref):
            pickings = self.env["stock.picking"].browse(res_ids)
            pickings.write({"picking_printed": fields.Datetime.now()})

        return super()._render_qweb_pdf(report_ref, res_ids=res_ids, data=data)
