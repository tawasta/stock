from odoo import fields, models


class StockPicking(models.Model):
    _inherit = ["stock.picking", "partner.warning.mixin"]

    _warning_message_field = "picking_warn_msg"
    _warning_level_field = "picking_warn_level"

    partner_picking_warn_level = fields.Selection(
        related="partner_id.picking_warn_level"
    )
