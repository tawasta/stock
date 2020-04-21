import base64
import urllib.request

from odoo import fields, http, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    barcode = fields.Binary(string="Barcode URL", compute="_barcode",)

    barcode_url = fields.Char(string="Barcode URL", compute="_barcode_url",)

    def _barcode(self):
        url = self._barcode_url()
        img = urllib.request.urlopen(url).read()
        self.barcode = base64.b64encode(img)

    def _barcode_url(self, code="Code128"):
        url = "{}{}{}{}{}".format(
            http.request.env["ir.config_parameter"].get_param("web.base.url"),
            "/report/barcode/",
            code,
            "/",
            self.name,
        )
        self.barcodeurl = url
        return url
