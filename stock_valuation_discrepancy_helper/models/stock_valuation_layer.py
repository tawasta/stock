from odoo import api
from odoo import _
from odoo import fields
from odoo import models
from odoo.exceptions import ValidationError


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    remaining_qty_discrepancy = fields.Boolean(
        "Quantity discrepancy",
        help="Remaining quantity exceeds the quantity. This isn't possible",
        store=True,
        compute="_compute_remaining_qty_discrepancy",
    )

    unit_cost_discrepancy = fields.Monetary(
        "Value discrepancy",
        compute="_compute_unit_cost_discrepancy",
        store=True,
    )

    @api.depends("remaining_qty", "quantity")
    def _compute_remaining_qty_discrepancy(self):
        for record in self:
            discrepancy = 0 <= record.quantity < record.remaining_qty
            record.remaining_qty_discrepancy = discrepancy

    @api.depends("remaining_qty", "quantity", "unit_cost")
    def _compute_unit_cost_discrepancy(self):
        for record in self:
            diff = record.unit_cost - record.product_id.standard_price
            record.remaining_qty_discrepancy = diff

    def action_sync_remaining_value(self):
        for record in self:
            if record.quantity < 0:
                raise ValidationError(_("Remaining quantity can't be negative"))

            if record.remaining_qty_discrepancy and record.quantity >= 0:
                record.remaining_qty = record.quantity

            record._compute_remaining_qty_discrepancy()
