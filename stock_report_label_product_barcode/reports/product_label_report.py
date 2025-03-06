from collections import defaultdict

from odoo import models, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class ReportProductTemplateLabelBarcodeAsBarcode(models.AbstractModel):
    _name = "report.stock_report_label_product_barcode.barcode_as_barcode"
    _description = "Product Label Report: Barcode as Barcode"

    def _get_report_values(self, docids, data):
        """ """

        layout_wizard = self.env["product.label.layout"].browse(
            data.get("layout_wizard")
        )

        # Only allow printing barcode labels for variants
        if data.get("active_model") == "product.product":
            Product = self.env["product.product"].with_context(
                display_default_code=False
            )
        else:
            raise UserError(
                _("Product model not defined, Please contact your administrator.")
            )

        if not layout_wizard:
            return {}

        # Check how many labels of each product should be printed.
        # Logic imitated from core.

        qty_by_product_in = data.get("quantity_by_product")
        # search for products all at once, ordered by name desc since popitem() used in xml to print the labels
        # is LIFO, which results in ordering by product name in the report
        products = Product.search(
            [("id", "in", [int(p) for p in qty_by_product_in.keys()])],
            order="name desc",
        )
        quantity_by_product = defaultdict(list)
        for product in products:
            q = qty_by_product_in[str(product.id)]
            quantity_by_product[product].append((product.barcode, q))

        _logger.info("qty by product ================")
        _logger.info(quantity_by_product)

        return {
            "quantity": quantity_by_product,
        }
