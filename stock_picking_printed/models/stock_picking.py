from odoo import fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    picking_printed = fields.Datetime(
        string="Picking printed", default=False, copy=False
    )
