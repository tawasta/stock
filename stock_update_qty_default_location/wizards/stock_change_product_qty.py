from odoo import api, models


class ProductChangeQuantity(models.TransientModel):

    _inherit = "stock.change.product.qty"

    @api.model
    def default_get(self, fields):
        res = super(ProductChangeQuantity, self).default_get(fields)

        if self.env.user.company_id.stock_update_qty_location_default:
            res['location_id'] = self.env.user.company_id \
                .stock_update_qty_location_default.id

        return res
