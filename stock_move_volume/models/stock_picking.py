# -*- coding: utf-8 -*-


from odoo import fields, models
from odoo.addons import decimal_precision as dp


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    total_volume = fields.Float(
        string="Total Volume",
        digits_compute=dp.get_precision('Stock Weight'),
    )

    def calculate_volume(self, context=None):
        """ Calculate the total for the whole
        picking by summing the line volumes """

        total = 0.0
        for line in self.move_lines:
            total += line.product_id.volume * line.product_uom_qty

        self.total_volume = total

        return {}
