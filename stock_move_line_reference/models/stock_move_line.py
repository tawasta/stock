from odoo import fields, models


class StockMoveLine(models.Model):

    _inherit = "stock.move.line"

    picking_id = fields.Many2one(string="Transfer Reference")
