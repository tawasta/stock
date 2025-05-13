from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _create_picking(self):
        res = super()._create_picking()

        for order in self.filtered(lambda po: po.state in ("purchase", "done")):
            for picking in order.picking_ids:
                if picking.picking_type_id.unreserve_receipt:
                    picking.do_unreserve()
        return res
