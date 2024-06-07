from odoo import fields, models


class StockPickingDelayReason(models.Model):

    _inherit = "stock.picking.delay.reason"

    delay_details = fields.One2many(
        string="Delay Details",
        comodel_name="stock.picking.delay.detail",
        inverse_name="delay_reason",
    )
