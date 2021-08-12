
from odoo import api, models


class StockQuantityHistory(models.TransientModel):
    _inherit = 'stock.quantity.history'

    def _prepare_stock_inventory_valuation_report(self):
        self.ensure_one()
        res = super()._prepare_stock_inventory_valuation_report()

        if self.location_id.id:
            res['location_id'] = self.location_id.id

        return res
