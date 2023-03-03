from odoo import fields, models


class StockMoveLine(models.Model):

    _inherit = "stock.move.line"

    partner_id = fields.Many2one("res.partner", related="picking_id.partner_id")
