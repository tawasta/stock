from odoo import models


class StockMove(models.Model):

    _inherit = "stock.move"

    def _trigger_assign(self):
        """Return nothing and do not reserve anything. Search
        this function in 'stock' module to better understand
        how this module works."""
        return
