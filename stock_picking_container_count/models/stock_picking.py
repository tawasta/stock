# -*- coding: utf-8 -*-


from odoo import fields, models


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    container_count = fields.Integer(
        string="Number of containers",
        default=1,
    )
