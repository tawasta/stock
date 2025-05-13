from odoo import models


class StockBackorderConfirmation(models.TransientModel):
    _inherit = "stock.backorder.confirmation"

    def sudo_process(self):
        return super(StockBackorderConfirmation, self.sudo()).process()

    def sudo_process_cancel_backorder(self):
        return super(StockBackorderConfirmation, self.sudo()).process_cancel_backorder()
