from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    remaining_qty_discrepancy = fields.Boolean(
        "Quantity discrepancy",
        help="Remaining quantity exceeds the quantity. This isn't possible",
        store=True,
        compute="_compute_remaining_qty_discrepancy",
    )

    cumulative_quantity = fields.Float(
        "Cumulative Quantity",
        digits=0,
        help="Quantity at this point, without considering consumed units",
        compute="_compute_cumulative_quantity",
    )

    unit_cost_discrepancy = fields.Monetary(
        "Value discrepancy",
        help="The difference between current valuation cost and product unit cost",
        compute="_compute_unit_cost_discrepancy",
        store=True,
    )

    product_on_hand = fields.Float(
        "On hand",
        digits=0,
        help="Products on hand at the current moment, doesn't show history",
        compute="_compute_product_on_hand",
    )

    @api.depends("remaining_qty", "quantity")
    def _compute_remaining_qty_discrepancy(self):
        for record in self:
            discrepancy = 0 <= record.quantity < record.remaining_qty
            record.remaining_qty_discrepancy = discrepancy

    def _compute_cumulative_quantity(self):
        for record in self:
            layers = self.search(
                [
                    ("product_id", "=", record.product_id.id),
                    ("create_date", "<=", record.create_date),
                ]
            )
            qty = sum(layers.mapped("quantity"))
            record.cumulative_quantity = qty

    @api.depends("remaining_qty", "quantity", "unit_cost")
    def _compute_unit_cost_discrepancy(self):
        for record in self:
            diff = record.unit_cost - record.product_id.standard_price
            record.unit_cost_discrepancy = diff

    @api.depends("product_id")
    def _compute_product_on_hand(self):
        for record in self:
            record.product_on_hand = record.product_id.qty_available

    def action_sync_remaining_qty(self):
        raise ValidationError(_("Disabled"))
        for record in self:
            if record.quantity < 0:
                raise ValidationError(_("Remaining quantity can't be negative"))
            elif record.quantity > record.remaining_qty:
                raise ValidationError(
                    _("Changing remaining quantity for consumed line not allowed")
                )

            record.remaining_qty = record.quantity
            record.remaining_value = record.quantity * record.unit_cost
            record._compute_remaining_qty_discrepancy()

    def action_clear_remaining_qty(self):
        raise ValidationError(_("Disabled"))
        self.write({"remaining_qty": 0, "remaining_value": 0})
