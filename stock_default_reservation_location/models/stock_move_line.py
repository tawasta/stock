from odoo import api, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.model_create_multi
    def create(self, vals_list):
        """Check first if products are available in default location of a product.
        If products are not available there, use another available location. Search
        is done for stock quants and they are ordered by their ID naturally. So this
        function mimics the behaviour of standard odoo"""
        for vals in vals_list:
            product_id = vals.get("product_id", False)

            move_id = vals.get("move_id", False)
            move = self.env["stock.move"].browse(move_id)
            picking_type_id = move and move.picking_type_id or False
            use_default = (
                picking_type_id and picking_type_id.use_default_location or False
            )

            if product_id and use_default:
                product = self.env["product.product"].browse(product_id)
                default_location = product.default_stock_move_location_id or False

                uom_id = vals.get("product_uom_id", False)
                company_id = vals.get("company_id", False)
                quantity = vals.get("quantity", False)
                quant_candidate_found = False
                if uom_id and company_id and quantity:
                    quant_candidate_found = self.env["stock.quant"].search(
                        [
                            ("product_id", "=", product_id),
                            ("product_uom_id", "=", uom_id),
                            ("company_id", "=", company_id),
                        ]
                    )
                    quant_candidate_found = quant_candidate_found.filtered(
                        lambda q, quantity=quantity: q.inventory_quantity_auto_apply
                        >= quantity
                    )
                    quants_found_by_default_location = quant_candidate_found.filtered(
                        lambda q, default_location=default_location: q.location_id.id
                        == default_location.id
                    )
                    quants_found_by_location = quant_candidate_found.filtered(
                        lambda q: q.location_id.usage == "internal"
                    )
                if default_location and quants_found_by_default_location:
                    vals["location_id"] = default_location.id
                elif quants_found_by_location:
                    vals["location_id"] = quants_found_by_location[0].location_id.id

        return super().create(vals_list)
