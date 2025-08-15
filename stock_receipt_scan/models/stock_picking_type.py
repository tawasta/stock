from odoo import models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    def action_open_barcode_transfer_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Transfer wizard",
            "res_model": "stock.barcode.transfer.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_wizard_mode": self.code,
                "default_picking_type_id": self.id,
            },
        }
