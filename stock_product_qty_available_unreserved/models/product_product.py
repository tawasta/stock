from odoo import fields, models

from odoo.addons import decimal_precision as dp


class ProductProduct(models.Model):
    # 1. Private attributes
    _inherit = "product.product"

    # 2. Fields declaration
    qty_available_unreserved = fields.Float(
        string="Unreserved quantity on hand",
        compute="_compute_quantities",
        search="_search_qty_available_unreserved",
        digits=dp.get_precision("Product Unit of Measure"),
    )

    # 3. Default methods

    # 4. Compute and search fields, in the same order that fields declaration
    def _compute_quantities(self):
        res = super()._compute_quantities()
        for product in self:
            unreserved = product.qty_available - product.outgoing_qty
            product.qty_available_unreserved = unreserved
        return res

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods

    # 8. Business methods
