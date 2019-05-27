
# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import fields, models, _
from odoo.addons import decimal_precision as dp

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class StockPicking(models.Model):

    # 1. Private attributes
    _inherit = 'stock.picking'

    # 2. Fields declaration
    weight_pack_operations = fields.Float(
        'Weight', digits=dp.get_precision('Weight'),
        compute='_compute_weight',
        help=_('Total weight for "To Do" operations')
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    def _compute_weight(self):
        for record in self:
            weight = 0
            for line in record.pack_operation_product_ids:
                weight += line.weight

            record.weight_pack_operations = weight

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
