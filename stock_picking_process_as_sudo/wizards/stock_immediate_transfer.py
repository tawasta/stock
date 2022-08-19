from odoo import models


class StockImmediateTransfer(models.TransientModel):
    _inherit = "stock.immediate.transfer"

    def sudo_process(self):
        return self.sudo().process()
