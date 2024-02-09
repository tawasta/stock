from odoo import api, fields, models


class StockMove(models.Model):

    _inherit = "stock.move"

    carrier_id = fields.Many2one(
        "delivery.carrier", compute="_compute_carrier_id", store=True
    )

    def picking_with_carrier(self):
        moves = self.env["stock.move"].search([]).sorted(key=lambda m: m.id)
        for move in moves:
            if move.picking_id.carrier_id:
                yield move

    @api.depends("picking_id", "picking_id.carrier_id")
    def _compute_carrier_id(self):
        moves = self.picking_with_carrier()
        for move in moves:
            move.carrier_id = move.picking_id.carrier_id
