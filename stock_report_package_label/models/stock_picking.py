from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def print_package_label(self):
        report = self.env.ref("stock_report_package_label.print_package_label")

        return report.report_action(self)
