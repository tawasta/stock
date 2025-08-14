from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_open_barcode_transfer_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Transfer wizard",
            "res_model": "stock.barcode.transfer.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_picking_id": self.id,
            },
        }

    def action_open_barcode_scan_wizard(self):
        raise Exception("Deprecated")
        return {
            "type": "ir.actions.act_window",
            "name": "Scan Barcode",
            "res_model": "barcode.scan.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_picking_id": self.id,
            },
        }
