from odoo.models import TransientModel


class StockPickingMassAction(TransientModel):

    _inherit = "stock.picking.mass.action"

    def mass_action(self):
        if self.transfer:
            for pick in self.picking_ids:
                pick.mass_transfer_done = True
        return super(StockPickingMassAction, self).mass_action()
