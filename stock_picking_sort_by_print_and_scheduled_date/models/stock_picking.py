
from odoo import models


class StockPicking(models.Model):

    _inherit = "stock.picking"
    _order = "picking_printed desc, scheduled_date desc"
