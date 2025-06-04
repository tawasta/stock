from odoo import _, fields, models


class StockWarehouseOrderpoint(models.Model):
    _name = "stock.warehouse.orderpoint"
    _inherit = ["stock.warehouse.orderpoint", "mail.thread"]

    # Stored field which is used for alerts, not its computed counterpart
    qty_on_hand_to_check = fields.Float(
        store=True,
        copy=False,
        default=lambda self: self._default_qty_on_hand_to_check(),
    )

    def _default_qty_on_hand_to_check(self):
        return self.qty_on_hand

    def cron_qty_on_hand_alert(self):
        """Check if quantity drops below minimium quantity. Send a message
        if a responsible is found from product. Don't send a message if it
        has been previously sent and the quantity has not changed after
        earlier message."""

        orderpoints = self.env["stock.warehouse.orderpoint"].search([])

        for orderpoint in orderpoints:
            responsible = (
                orderpoint.product_id and orderpoint.product_id.responsible_id or False
            )
            responsible_email = responsible and responsible.partner_id.email or False
            quantity_has_changed = (
                orderpoint.qty_on_hand_to_check != orderpoint.qty_on_hand
            )

            if (
                orderpoint.qty_on_hand < orderpoint.product_min_qty
                and responsible_email
                and quantity_has_changed
            ):
                display_msg = _(
                    """<div style="color: red;">
                    Replenishment for location: {}
                    <br/>
                    The quantity of {} product is below its minimium quantity ({}) and it is now {}
                    </div>
                    """.format(
                        orderpoint.location_id and orderpoint.location_id.name or "",
                        orderpoint.product_id.display_name,
                        orderpoint.product_min_qty,
                        orderpoint.qty_on_hand,
                    )
                )

                orderpoint.message_post(
                    message_type="notification",
                    subject=_(
                        """Alert because the quantity on hand of product {} has dropped
                       below its minimium quantity""".format(
                            orderpoint.product_id.display_name,
                        )
                    ),
                    body=display_msg,
                    partner_ids=[responsible.partner_id.id],
                    body_is_html=True,
                )

            orderpoint.qty_on_hand_to_check = orderpoint.qty_on_hand
