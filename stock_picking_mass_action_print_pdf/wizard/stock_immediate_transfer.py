
from odoo import fields, models


class StockImmediateTransfer(models.TransientModel):

    _inherit = 'stock.immediate.transfer'

    mass_transfer_done = fields.Boolean(default=False)

    def process(self):
        super(StockImmediateTransfer, self).process()
        pickings = self.pick_ids.filtered(
            lambda x: x.mass_transfer_done).sorted(key=lambda t: t.id)
        picks = False
        if pickings:
            self.mass_transfer_done = True
            picks = self.env.ref('stock.action_report_picking').\
                report_action(pickings)
        return picks
