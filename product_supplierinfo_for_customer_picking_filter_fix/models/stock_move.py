from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.depends(
        "picking_id.partner_id", "product_id", "product_id.customer_ids.product_code"
    )
    def _compute_product_customer_code(self):
        """Copy-pasted code, but the filter has been fixed"""
        for move in self:
            product_customer_code = False
            if (
                move.picking_id
                and move.picking_id.partner_id
                and move.product_tmpl_id.customer_ids
            ):
                # Here is the fix
                customer = fields.first(
                    move.product_tmpl_id.customer_ids.filtered(
                        lambda m: move.picking_id.partner_id == m.name
                    )
                )

                product_customer_code = customer.product_code
            move.product_customer_code = product_customer_code
