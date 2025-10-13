import logging
import re
from datetime import datetime

from odoo import _, api, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.onchange("barcode")
    def onchange_barcode_parse_contents(self):
        """If barcode contains GS1 format, parse it to correct fields"""
        for record in self:
            if record.barcode and "(" in record.barcode:
                parsed_barcode = record.parse_gs1_barcode(record.barcode)
                record.barcode = parsed_barcode.get("barcode")
                record.default_code = parsed_barcode.get("product_code")

    def parse_gs1_barcode(self, barcode_str):
        """Parse a GS1 barcode string and extract relevant information"""
        _logger.debug("Parsing barcode: %s", barcode_str)

        # Regular expression to match (AI)(value) pairs
        pattern = r"\((\d{2,3})\)([^\(]+)"
        parsed_barcode = {
            ai: value.strip() for ai, value in re.findall(pattern, barcode_str)
        }

        barcode = parsed_barcode.get("01")
        lot_name = parsed_barcode.get("10")
        expiration_raw = parsed_barcode.get("17")
        product_code = parsed_barcode.get("240")

        if expiration_raw and re.match(r"^\d{6}$", expiration_raw):
            try:
                expiration_date = datetime.strptime(expiration_raw, "%y%m%d").date()
            except ValueError as err:
                raise UserError(_("Invalid expiration date format.")) from err
        else:
            expiration_date = None

        values = {
            "barcode": barcode,
            "product_code": product_code,
            "lot_name": lot_name,
            "expiration_date": expiration_date,
        }
        _logger.debug("Parse results: %s", values)

        return values
