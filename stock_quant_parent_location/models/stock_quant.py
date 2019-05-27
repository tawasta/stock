from odoo import models, fields


class StockQuant(models.Model):

    _inherit = 'stock.quant'

    parent_location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Parent Location',
        related='location_id.location_id'
    )
