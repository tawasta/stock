from odoo import models


class StockBackorderConfirmation(models.TransientModel):
    _inherit = "stock.backorder.confirmation"

    def sudo_process(self):
        self.sudo().process()

    def sudo_process_cancel_backorder(self):
        self.sudo().process_cancel_backorder()
