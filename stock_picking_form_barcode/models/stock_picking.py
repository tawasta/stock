import base64
import ssl
import urllib.request

from odoo import fields, http, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    barcode = fields.Binary(string="Barcode URL", compute="_barcode")
    barcode_url = fields.Char(string="Barcode URL", compute="_barcode_url")

    def _barcode(self):
        for record in self:
            if isinstance(record.barcode_url, str) \
                    and len(record.barcode_url) > 0:
                img = urllib.request.urlopen(record.barcode_url).read()
                record.barcode = base64.b64encode(img)

    def _barcode_url(self, code="EAN13"):
        for record in self:
            ssl._create_default_https_context = ssl._create_unverified_context
            if isinstance(record.name, str) and len(record.name) > 0:
                record.barcode_url = "{}{}{}{}{}".format(
                    http.request.env["ir.config_parameter"]
                    .sudo()
                    .get_param("web.base.url"),
                    "/report/barcode/",
                    code,
                    "/",
                    record.name,
                )
                record.barcode_url = record.barcode_url.replace("//", "/")
                record.barcode_url = \
                    record.barcode_url.replace("https:/", "https://")
                record.barcode_url = \
                    record.barcode_url.replace("http:/", "http://")
            else:
                record.barcode__url = ""
