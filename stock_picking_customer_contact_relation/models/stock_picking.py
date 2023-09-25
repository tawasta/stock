from odoo import fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    customer_contact = fields.Many2one(
        "res.partner", related="sale_id.customer_contact_id"
    )
