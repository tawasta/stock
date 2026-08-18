from odoo import models


class ReportLabelZd620Lot(models.AbstractModel):
    _name = "report.stock_label_zebra_zd620.label_zd620_lot_view"
    _description = "ZD620 Lot Label Data"

    def _get_report_values(self, docids, data):
        return {
            "docs": self.env["stock.lot"].browse(docids),
            "company": self.env.company,
        }
