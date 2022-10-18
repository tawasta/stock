from odoo import fields, models


class StockImmediateTransfer(models.TransientModel):

    _inherit = "stock.immediate.transfer"

    mass_transfer_done = fields.Boolean(default=False)

    def process(self):
        super(StockImmediateTransfer, self).process()
        pickings = self.pick_ids.sorted(key=lambda t: t.id).print_delivery_slip()

        if pickings:
            self.mass_transfer_done = True
            return pickings
