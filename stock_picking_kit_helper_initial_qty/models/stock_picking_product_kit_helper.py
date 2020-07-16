
from odoo import fields, models


class StockPickingProductKitHelper(models.Model):

    _inherit = "stock.picking.product.kit.helper"

    ordered_quantity = fields.Float(related="sale_line_id.product_uom_qty")
