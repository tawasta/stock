from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    created_from_stock_move = fields.One2many(
        comodel_name="stock.move", inverse_name="manufacturing_order_id"
    )
