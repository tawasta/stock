from odoo import fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    mass_transfer_done = fields.Boolean(copy=False, default=False)

    def print_delivery_slip(self):
        pickings = self.filtered(lambda x: not x.purchase_id)

        picks = False
        if pickings:
            picks = self.env.ref("stock.action_report_delivery").report_action(pickings)
        return picks
