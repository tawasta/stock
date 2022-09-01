
from odoo import fields, models


class StockPickin(models.Model):

    _inherit = 'stock.picking'

    user_id = fields.Many2one(related="sale_id.user_id")
