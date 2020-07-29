
from odoo import api
from odoo.models import TransientModel


class StockPickingMassAction(TransientModel):

    _inherit = 'stock.picking.mass.action'

    @api.multi
    def print_mass_pdf(self):
        pickings = self.picking_ids
        picks = self.env.ref('stock.action_report_picking').\
            report_action(pickings)
        return picks

    @api.multi
    def mass_action(self):
        res = super(StockPickingMassAction, self).mass_action()
        if self.transfer:
            for pick in self.picking_ids:
                pick.mass_transfer_done = True
        return res
