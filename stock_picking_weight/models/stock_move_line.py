
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class StockMoveLine(models.Model):

    _inherit = 'stock.move.line'

    weight = fields.Float(
        'Weight', digits=dp.get_precision('Weight'),
        compute='_compute_weight',
    )

    # Compute and search fields, in the same order that fields declaration
    @api.onchange('product_id', 'product_uom_id', 'product_qty')
    def _compute_weight(self):
        for record in self:
            uom_weight = record.product_id.uom_id._compute_weight(
                record.product_id.weight,
                record.product_uom_id,
            )

            # Negative quantity doesn't have a weight
            uom_qty = record.product_qty if record.product_qty > 0 else 0

            weight = uom_qty * uom_weight

            record.weight = weight
