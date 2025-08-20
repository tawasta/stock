import logging

from odoo import models

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_open_barcode_transfer_wizard(self):
        context = {
            # Tell the wizard to limit the picking to the current one
            "default_picking_id": self.id,
            # Tell the wizard what kind of move we are making
            "default_picking_type_id": self.picking_type_id.id,
            # Tell the wizard the source and destination locations
            "default_location_src_id": self.location_id.id,
            "default_location_dest_id": self.location_dest_id.id,
        }

        _logger.debug(context)

        return {
            "type": "ir.actions.act_window",
            "name": "Transfer wizard",
            "res_model": "stock.barcode.transfer.wizard",
            "view_mode": "form",
            "target": "new",
            "context": context,
        }
