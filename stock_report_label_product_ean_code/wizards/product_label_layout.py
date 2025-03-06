from odoo import _, api, fields, models
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class ProductLabelLayout(models.TransientModel):
    _inherit = "product.label.layout"

    print_format = fields.Selection(
        selection_add=[("ean_as_barcode", "Product Sticker: Product EAN as Barcode")],
        ondelete={"ean_as_barcode": "set default"},
    )

    def _prepare_report_data(self):
        """
        If EAN as Barcode was selected in Print Labels wizard,
        switch to the corresponding template
        """
        xml_id, data = super()._prepare_report_data()

        if self.print_format == "ean_as_barcode":
            xml_id = "stock_report_label_product_ean_code.report_product_product_label_ean_as_barcode"

        return xml_id, data
