from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Product(models.Model):
    _inherit = "product.product"

    def action_sync_with_on_hand(self):
        raise ValidationError(_("Disabled"))
        svl = self.env["stock.valuation.layer"]
        for record in self:
            layers = svl.search([("product_id", "=", record.id)], order="create_date DESC")
            layer0 = layers[0]

            qty = sum(layers.mapped("quantity"))
            remaining_qty = sum(layers.mapped("remaining_qty"))

            if qty != record.qty_available:
                new_qty = -(qty-record.qty_available)
                new_remaining_qty = -(remaining_qty-record.qty_available)
                unit_cost = record.standard_price
                values = {
                    "product_id": record.id,
                    "quantity": new_qty,
                    "remaining_qty": new_remaining_qty,
                    "uom_id": record.uom_id.id,
                    "company_id": layer0.company_id.id,
                    "unit_cost": unit_cost,
                    "value": unit_cost * new_qty,
                    "description": "Valuation synchronization",
                }

                svl.create(values)
