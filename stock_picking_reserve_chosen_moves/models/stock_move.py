
from odoo import fields, models


class StockMove(models.Model):

    _inherit = 'stock.move'

    reserve_this_move = fields.Boolean(string="Reserve", default=False)
