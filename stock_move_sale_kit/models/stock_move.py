##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2022- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

# 1. Standard library imports:
import base64
import logging
import ssl
import urllib.parse
import urllib.request

import requests

# 2. Known third party imports:
# 3. Odoo imports (openerp):
from odoo import fields, http, models

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:

_logger = logging.getLogger(__name__)


class StockMoveLine(models.Model):
    # 1. Private attributes
    _inherit = "stock.move.line"

    # 2. Fields declaration
    sale_line_id = fields.Many2one(related="move_id.sale_line_id")
    sale_line_kit = fields.Many2one(
        string="Sales Package",
        comodel_name="product.product",
        compute="_compute_sale_line_kit",
    )
    sale_line_kit_barcode = fields.Char(string="EAN13", related="sale_line_kit.barcode")
    sale_line_kit_default_code = fields.Char(
        string="Product Code", related="sale_line_kit.default_code"
    )
    barcode_image = fields.Image(
        string="EAN13 Barcode", compute="_compute_barcode_image", readonly="True"
    )
    reference_barcode_image = fields.Image(
        string="Reference Barcode",
        compute="_compute_reference_barcode_image",
        readonly="True",
    )
    default_code_barcode_image = fields.Image(
        string="Product Code Barcode",
        compute="_compute_default_code_barcode_image",
        readonly="True",
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    def _compute_sale_line_kit(self):
        for line in self:
            if line.sale_line_id:
                bom = (
                    self.env["mrp.bom"]
                    .sudo()
                    ._bom_find(
                        product=line.sale_line_id.product_id,
                        company_id=line.picking_id.company_id.id,
                    )
                )
                if bom.type == "phantom":
                    line.sale_line_kit = line.sale_line_id.product_id
                else:
                    line.sale_line_kit = None
            else:
                line.sale_line_kit = None

    def _compute_barcode_image(self):
        for line in self:
            if line.sale_line_kit_barcode:
                line.barcode_image = line._get_barcode(line.sale_line_kit_barcode)
            else:
                line.barcode_image = None

    def _compute_reference_barcode_image(self):
        for line in self:
            if line.reference:
                line.reference_barcode_image = line._get_barcode(line.reference)
            else:
                line.reference_barcode_image = None

    def _compute_default_code_barcode_image(self):
        for line in self:
            if line.sale_line_kit_default_code:
                line.default_code_barcode_image = line._get_barcode(
                    line.sale_line_kit_default_code
                )
            else:
                line.default_code_barcode_image = None

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    def _get_barcode(self, data, code="EAN13"):
        self.ensure_one()
        ssl._create_default_https_context = ssl._create_unverified_context
        if isinstance(data, str) and len(data) > 0:
            url = "{}{}{}{}{}".format(
                http.request.env["ir.config_parameter"]
                .sudo()
                .get_param("web.base.url"),
                "/report/barcode/",
                urllib.parse.quote(code),
                "/",
                urllib.parse.quote(data),
            )
            url = url.replace(" ", "")
            url = url.replace("//", "/")
            url = url.replace("https:/", "https://")
            url = url.replace("http:/", "http://")
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    image_data = base64.b64encode(
                        requests.get(url, timeout=10).content
                    ).replace(b"\n", b"")
                    return image_data
                else:
                    _logger.warning("Unable to load the image from URL %s." % url)
                    return None
            except Exception as err:
                _logger.warning("Unable to load the image from URL %s." % url)
                _logger.warning(err)
                return None
        else:
            return None

    # 8. Business methods
