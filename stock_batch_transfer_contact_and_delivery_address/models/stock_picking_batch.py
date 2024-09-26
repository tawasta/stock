from odoo import fields, models


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    delivery_address_id = fields.Many2one(
        "res.partner",
        string="Delivery Address",
    )

    customer_contact_id = fields.Many2one(
        "res.partner",
        string="Contact",
    )
