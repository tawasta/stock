from odoo import fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    mass_transfer_done = fields.Boolean(default=False)

    def print_delivery_slip(self):
        pickings = self.filtered(lambda x: x.mass_transfer_done).sorted(
            key=lambda t: t.id
        )
        picks = False
        if pickings:
            for picking in pickings:
                picking.mass_transfer_done = True
            picks = self.env.ref("stock.action_report_delivery").report_action(pickings)
        return picks
