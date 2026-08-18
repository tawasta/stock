from odoo import models

from odoo.addons.product.report.product_label_report import _prepare_data


class ReportLabelZd620Product(models.AbstractModel):
    _name = "report.stock_label_zebra_zd620.label_zd620_product_view"
    _description = "ZD620 Product Label Data"

    def _get_report_values(self, docids, data):
        values = _prepare_data(self.env, docids, data)
        values["company"] = self.env.company
        return values
