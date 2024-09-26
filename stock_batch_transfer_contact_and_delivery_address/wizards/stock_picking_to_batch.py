from odoo import models


class StockPickingToBatch(models.TransientModel):
    _inherit = "stock.picking.to.batch"

    def attach_pickings(self):
        """Search Delivery type address from customer's contacts.
        This Address should also be set as a company. Use customer
        as a contact if this customer is not a company."""
        res = super().attach_pickings()

        pickings = self.env["stock.picking"].browse(self.env.context.get("active_ids"))

        delivery_address = False
        customer_contact = False

        for picking in pickings:
            sale = picking.sale_id
            if sale:
                delivery_address = sale.partner_id.child_ids.filtered(
                    lambda add: add.type == "delivery" and add.is_company
                )
                customer_contact = (
                    not sale.partner_id.is_company and sale.partner_id or False
                )

            if customer_contact and delivery_address:
                break

        batch = pickings and pickings[0] and pickings[0].batch_id or False

        batch.delivery_address_id = delivery_address
        batch.customer_contact_id = customer_contact

        return res
