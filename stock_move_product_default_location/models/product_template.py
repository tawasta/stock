from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    default_stock_move_location_id = fields.Many2one(
        "stock.location",
        string="Default Stock move Location",
    )
