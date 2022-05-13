
from odoo import api, models


class StockMove(models.Model):

    _inherit = 'stock.move'

    @api.model
    def create(self, vals):
        group_id = vals.get('group_id', False)
        if group_id:
            group = self.env['procurement.group'].search([('id', '=', group_id)])
            group.force_unreserve = True

        return super().create(vals)
