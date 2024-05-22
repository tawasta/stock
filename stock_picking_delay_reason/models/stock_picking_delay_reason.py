from odoo import fields, models

class StockPickingDelayReason(models.Model):

    _name = "stock.picking.delay.reason"

    name = fields.Char(string="Reason", required=True)