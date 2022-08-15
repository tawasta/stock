from odoo import fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    comment = fields.Text(
        help="Add a comment that will be printed on the Delivery Slip",
    )
