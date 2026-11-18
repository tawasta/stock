from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    valued = fields.Boolean(
        related=False,
        compute="_compute_valued",
        help="Set only when the delivery slip is printed with prices.",
    )

    @api.depends_context("delivery_slip_valued")
    def _compute_valued(self):
        # The chosen print decides whether prices are shown,
        # not the partner's valued picking setting.
        self.valued = bool(self.env.context.get("delivery_slip_valued"))
