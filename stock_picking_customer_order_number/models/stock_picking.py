from odoo import fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    customer_order_number = fields.Char(
        string="Customer Order Number",
        related="sale_id.customer_order_number",
        stored=True,
    )
