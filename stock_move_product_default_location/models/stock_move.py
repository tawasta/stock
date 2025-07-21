from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    def write(self, vals):
        res = super().write(vals)

        product_id = vals.get("product_id", False)

        if product_id:
            product = self.env["product.product"].browse(product_id)
            default_location = product.default_stock_move_location_id or False
            if default_location:
                vals["location_id"] = default_location.id

        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            product_id = vals.get("product_id", False)

            if product_id:
                product = self.env["product.product"].browse(product_id)
                default_location = product.default_stock_move_location_id or False
                if default_location:
                    vals["location_id"] = default_location.id

        return super().create(vals_list)
