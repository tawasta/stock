from odoo import fields, models


class StockQuant(models.Model):

    _inherit = 'stock.quant'

    value = fields.Monetary(groups='')
