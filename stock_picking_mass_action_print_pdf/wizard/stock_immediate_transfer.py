from odoo import fields, models


class StockImmediateTransfer(models.TransientModel):

    _inherit = "stock.immediate.transfer"

    mass_transfer_done = fields.Boolean(default=False)

    def process(self):
        super(StockImmediateTransfer, self).process()
        pickings = self.pick_ids.sorted(key=lambda t: t.id).print_delivery_slip()

        close_window = {"type": "ir.actions.act_window_close"}

        if pickings:
            return {"type": "ir.actions.act_multi", "actions": [pickings, close_window]}
