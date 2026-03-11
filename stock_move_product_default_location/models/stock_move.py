from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    def write(self, vals):
        product_id = vals.get("product_id", False)

        picking_type = self.picking_type_id
        code = picking_type and picking_type.code == "outgoing" or False

        if product_id and code:
            product = self.env["product.product"].browse(product_id)
            default_location = product.default_stock_move_location_id or False
            if default_location:
                vals["location_id"] = default_location.id

        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            product_id = vals.get("product_id", False)

            picking_type_id = vals.get("picking_type_id", False)
            picking_type = self.env["stock.picking.type"].browse(picking_type_id)
            code = picking_type and picking_type.code == "outgoing" or False

            if product_id and code:
                product = self.env["product.product"].browse(product_id)
                default_location = product.default_stock_move_location_id or False
                if default_location:
                    vals["location_id"] = default_location.id

        return super().create(vals_list)
