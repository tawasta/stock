from odoo import models


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        """Check if an order has Force Unreserve set to True and make
        reservertations based on that value."""
        res = super(SaleOrderLine, self)._action_launch_stock_rule(
            previous_product_uom_qty=previous_product_uom_qty
        )

        orders = list({x.order_id for x in self})

        for order in orders:
            if not order.force_unreserve:
                reassign = order.picking_ids.filtered(
                    lambda x: x.state == "confirmed"
                    or (x.state in ["waiting", "assigned"] and not x.printed)
                )

                if reassign:
                    reassign.action_confirm()
                    reassign.action_assign()

        return res
