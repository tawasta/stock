from odoo import fields, models


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    product_default_code = fields.Char(related="product_id.default_code", store=True)
