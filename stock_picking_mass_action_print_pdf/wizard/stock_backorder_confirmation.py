from odoo import fields, models


class StockBackorderConfirmation(models.TransientModel):

    _inherit = "stock.backorder.confirmation"

    mass_transfer_done = fields.Boolean(default=False)

    def process(self):
        res = super(StockBackorderConfirmation, self).process()
        pickings = self.pick_ids.print_delivery_slip()

        close_window = {"type": "ir.actions.act_window_close"}

        if pickings:
            self.mass_transfer_done = True
            return {"type": "ir.actions.act_multi", "actions": [pickings, close_window]}

        return {
            "type": "ir.actions.act_multi",
            "actions": [res, close_window],
        }

    def process_cancel_backorder(self):
        res = super(StockBackorderConfirmation, self).process_cancel_backorder()
        pickings = self.pick_ids.print_delivery_slip()

        close_window = {"type": "ir.actions.act_window_close"}

        if pickings:
            self.mass_transfer_done = True
            return {"type": "ir.actions.act_multi", "actions": [pickings, close_window]}

        return {
            "type": "ir.actions.act_multi",
            "actions": [res, close_window],
        }
