from odoo import api, fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    unreserve_receipt = fields.Boolean(
        string="Unreserve receipt automatically",
        copy=False,
        default=False,
        help="""Pickings created by this picking type will be unreserved
                automatically upon creating them.""",
    )
    hide_unreserve_receipt = fields.Boolean(compute="_compute_hide_unreserve_receipt")

    @api.depends("code")
    def _compute_hide_unreserve_receipt(self):
        for rec in self:
            rec.hide_unreserve_receipt = rec.code != "incoming"
