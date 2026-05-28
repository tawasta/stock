from odoo import api, fields, models
from odoo.tools import html2plaintext


class StockPicking(models.Model):
    _inherit = "stock.picking"

    has_note_text = fields.Boolean(
        string="Has note text",
        compute="_compute_has_note_text",
        store=True,
    )

    @api.depends("note")
    def _compute_has_note_text(self):
        for picking in self:
            text = html2plaintext(picking.note or "").strip()
            picking.has_note_text = bool(text)
