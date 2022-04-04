from odoo import _, api, models, fields


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    picking_id = fields.Many2one(comodel_name="stock.picking", related='move_id.picking_id', string="Transfer Reference", store=True, readonly=False)
