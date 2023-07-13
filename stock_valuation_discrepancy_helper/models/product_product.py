from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Product(models.Model):
    _inherit = "product.product"

    def action_sync_with_on_hand(self):
        svl = self.env["stock.valuation.layer"]
        for record in self:
            layers = svl.search([("product_id", "=", record.id)])

            qty = sum(layers.mapped("quantity"))

            if qty != record.qty_available:
                new_qty = -(qty-record.qty_available)
                values = {
                    "product_id": record.id,
                    "quantity": new_qty,
                    "remaining_qty": new_qty,
                    "uom_id": record.uom_id.id,
                    "company_id": record.company_id.id,
                    "unit_cost": record.standard_price,
                    "description": "Valuation synchronization",
                }

                svl.create(values)
