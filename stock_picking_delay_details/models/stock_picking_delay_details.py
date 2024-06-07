from odoo import fields, models


class StockPickingDelayDetail(models.Model):

    _name = "stock.picking.delay.detail"

    name = fields.Char(string="Delay detail", required=True)

    delay_reason = fields.Many2one(
        string="Delay Reason", comodel_name="stock.picking.delay.reason", required=True
    )
