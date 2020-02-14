
from odoo import fields, models
from odoo.addons import decimal_precision as dp


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    weight_pack_operations = fields.Float(
        'Weight', digits=dp.get_precision('Weight'),
        compute='_compute_weight',
        help='Total weight for "To Do" operations'
    )

    # Compute and search fields, in the same order that fields declaration
    def _compute_weight(self):
        for record in self:
            weight = 0
            for line in record.move_line_ids_without_package:
                weight += line.weight

            record.weight_pack_operations = weight
