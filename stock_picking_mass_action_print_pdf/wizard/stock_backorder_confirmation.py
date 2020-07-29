
from odoo import fields, models


class StockBackorderConfirmation(models.TransientModel):

    _inherit = 'stock.backorder.confirmation'

    mass_transfer_done = fields.Boolean(default=False)

    def process(self):
        super(StockBackorderConfirmation, self).process()
        pickings = self.pick_ids.filtered(lambda x: x.mass_transfer_done)
        picks = False
        if pickings:
            self.mass_transfer_done = True
            picks = self.env.ref('stock.action_report_picking').\
                report_action(pickings)
        return picks

    def process_cancel_backorder(self):
        super(StockBackorderConfirmation, self).process_cancel_backorder()
        pickings = self.pick_ids.filtered(lambda x: x.mass_transfer_done)
        picks = False
        if pickings:
            self.mass_transfer_done = True
            picks = self.env.ref('stock.action_report_picking').\
                report_action(pickings)
        return picks
