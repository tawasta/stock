from odoo import api, models


class ProductChangeQuantity(models.TransientModel):

    _inherit = "stock.change.product.qty"

    @api.model
    def default_get(self, fields):
        res = super(ProductChangeQuantity, self).default_get(fields)

        if self.env.user.company_id.default_stock_update_qty_location:
            res['location_id'] = self.env.user.company_id \
                .default_stock_update_qty_location.id

        return res
