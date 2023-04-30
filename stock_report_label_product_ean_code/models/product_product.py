from odoo import fields, models


class ProductProduct(models.Model):

    _inherit = "product.product"

    ean_code = fields.Char(string="EAN code", store=True)
