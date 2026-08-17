from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _update_standard_price(self, extra_value=None, extra_quantity=None):
        result = super()._update_standard_price(
            extra_value=extra_value, extra_quantity=extra_quantity
        )

        marked_up_products = self.filtered(
            lambda product: product.cost_method == "average"
            and product.categ_id.percentage_update
        )
        for product in marked_up_products:
            # Core already wrote the raw average cost above (under
            # disable_auto_revaluation, so no side effects); apply the
            # category's percentage markup on top of that written value.
            percentage = product.categ_id.percentage_update
            new_standard_price = product.standard_price * (1 + percentage)
            product.with_context(
                disable_auto_revaluation=True
            ).sudo().standard_price = new_standard_price

        return result
