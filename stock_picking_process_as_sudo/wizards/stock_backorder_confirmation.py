from odoo import models


class StockBackorderConfirmation(models.TransientModel):

    _inherit = "stock.backorder.confirmation"

    def sudo_process(self):
        close_window = {"type": "ir.actions.act_window_close"}

        return {
            "type": "ir.actions.act_multi",
            "actions": [self.sudo().process(), close_window],
        }

    def sudo_process_cancel_backorder(self):
        close_window = {"type": "ir.actions.act_window_close"}

        return {
            "type": "ir.actions.act_multi",
            "actions": [self.sudo().process_cancel_backorder(), close_window],
        }
