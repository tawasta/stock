from odoo import _, api, fields, models
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class ProductLabelLayout(models.TransientModel):
    _inherit = "product.label.layout"

    print_format = fields.Selection(
        selection_add=[("barcode_as_barcode", "Product Sticker: Product Barcode")],
        ondelete={"barcode_as_barcode": "set default"},
    )

    def _prepare_report_data(self):
        """
        If Product Barcode was selected in Print Labels wizard,
        switch to the corresponding template
        """
        xml_id, data = super()._prepare_report_data()

        if self.print_format == "barcode_as_barcode":
            xml_id = "stock_report_label_product_barcode.report_product_product_label_barcode_as_barcode"

        return xml_id, data
