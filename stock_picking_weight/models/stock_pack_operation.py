# -*- coding: utf-8 -*-

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class StockPackOperation(models.Model):

    # 1. Private attributes
    _inherit = 'stock.pack.operation'

    # 2. Fields declaration
    weight = fields.Float(
        'Weight', digits=dp.get_precision('Weight'),
        compute='_compute_weight',
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
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

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
