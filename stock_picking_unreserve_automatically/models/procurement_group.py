
from odoo import api, fields, models


class ProcurementGroup(models.Model):

    _inherit = 'procurement.group'

    force_unreserve = fields.Boolean(string="Force Unreserve", store=True)

    @api.model
    def create(self, vals):
        sale = vals.get('sale_id', False)
        sale = self.sudo().env['sale.order'].search([
            ('id', '=', sale)
        ])
        if sale:
            vals['force_unreserve'] = sale.force_unreserve
        return super().create(vals)
