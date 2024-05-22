from odoo import fields, models

class StockPicking(models.Model):

    _inherit = "stock.picking"

    delay_reason = fields.Many2one(string="Delay reason", comodel_name="stock.picking.delay.reason", store=True)