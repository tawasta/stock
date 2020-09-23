from odoo import fields, models


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    week_of_shipment = fields.Integer(related="sale_id.week_of_shipment")
