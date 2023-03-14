from odoo import fields, models


class StockMoveLine(models.Model):

    _inherit = "stock.move.line"

    initial_demand = fields.Float(
        string="Initial Demand", related="move_id.product_uom_qty"
    )
