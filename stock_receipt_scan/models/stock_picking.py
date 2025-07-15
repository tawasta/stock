from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_open_barcode_scan_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Scan Barcode',
            'res_model': 'barcode.scan.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_picking_id': self.id,
            }
        }

class StockMoveLineLog(models.Model):
    _inherit = 'stock.move.line'

    @api.model
    def create(self, vals):
        _logger.info("Creating stock.move.line with values:\n%s", vals)
        return super().create(vals)
