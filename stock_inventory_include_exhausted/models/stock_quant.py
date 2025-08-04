import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = "stock.quant"

    # Helper field for tracking/logging during initial use that this quant came
    # from an inventory where  include_exhausted was set to true. Not used in logic.
    zero_quant_from_inventory_adjustment = fields.Boolean(
        string="Zero quant originally created for inventory adjustments", default=False
    )

    @api.model
    def action_view_inventory(self):
        self.env["ir.config_parameter"].sudo().set_param("stock.skip_quant_tasks", True)
        return super().action_view_inventory()
