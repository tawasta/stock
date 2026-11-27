from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def print_package_label(self):
        self.ensure_one()
        report = self.env.ref("stock_report_package_label.print_package_label")
        if not self.sscc and self.partner_id.use_sscc_code:
            sscc_code = self.prepare_sscc_code()
            self.sscc = sscc_code

        return report.report_action(self)
