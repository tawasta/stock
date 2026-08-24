import base64
from io import BytesIO

from PIL import Image

from odoo import models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def _build_wkhtmltopdf_args(self, paperformat_id, landscape, **kwargs):
        """Force UTF-8: wkhtmltopdf's charset auto-detection is unreliable on these labels."""
        command_args = super()._build_wkhtmltopdf_args(
            paperformat_id, landscape, **kwargs
        )
        if paperformat_id and paperformat_id == self.env.ref(
            "stock_label_zebra_zd620.paperformat_zd620_label"
        ):
            command_args.extend(["--encoding", "utf-8"])
        return command_args

    def zd620_barcode_data_uri(self, value, humanreadable=True):
        """Same as core's barcode(), but with a transparent background."""
        if not value:
            return ""
        png_bytes = self.barcode(
            "auto", value, humanreadable=1 if humanreadable else 0, quiet=0
        )
        image = Image.open(BytesIO(png_bytes)).convert("RGBA")
        alpha = image.convert("L").point(lambda pixel: 0 if pixel > 200 else 255)
        image.putalpha(alpha)
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()
