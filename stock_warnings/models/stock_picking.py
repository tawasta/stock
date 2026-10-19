from odoo import models


class StockPicking(models.Model):
    _inherit = ["stock.picking", "partner.warning.mixin"]

    _warning_message_field = "picking_warn_msg"
    _warning_level_field = "picking_warn_level"
