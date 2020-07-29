
from odoo import fields, models


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    mass_transfer_done = fields.Boolean()
