from odoo import fields, models


class StockInventoryLine(models.Model):

    _inherit = "stock.inventory.line"

    tag_ids = fields.Many2many(
        comodel_name="product.template.tag",
        related="product_id.product_tmpl_id.tag_ids",
    )
