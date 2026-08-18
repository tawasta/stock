import base64
from io import BytesIO

from PIL import Image

from odoo import models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def zd620_barcode_data_uri(self, value, humanreadable=True):
        """Render a barcode the same way the core "barcode" QWeb widget
        does, but with its white background made transparent.

        The core widget always draws black bars on a white background
        (there's no color option in ir.actions.report.barcode()), and
        wkhtmltopdf doesn't support CSS mix-blend-mode to fake
        transparency, so the white square would otherwise stay visible on
        the label's colored background. Making the PNG itself transparent
        works in any renderer.
        """
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
