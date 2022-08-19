from odoo import fields, models


class StockBackorderConfirmation(models.TransientModel):

    _inherit = "stock.backorder.confirmation"

    mass_transfer_done = fields.Boolean(default=False)

    def process(self):
        super(StockBackorderConfirmation, self).process()
        pickings = self.pick_ids.print_delivery_slip()
        if pickings:
            self.mass_transfer_done = True
            return pickings

    def process_cancel_backorder(self):
        super(StockBackorderConfirmation, self).process_cancel_backorder()
        pickings = self.pick_ids.print_delivery_slip()
        if pickings:
            self.mass_transfer_done = True
            return pickings
