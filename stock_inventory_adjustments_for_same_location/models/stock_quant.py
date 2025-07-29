from odoo import _, models
from odoo.exceptions import UserError


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def _check_no_duplicate_line(self, inventory_ids, test_quants):
        domain = [
            ("product_id", "in", self.product_id.ids),
            ("location_id", "in", self.location_id.ids),
            "|",
            ("package_id", "in", self.package_id.ids),
            ("package_id", "=", None),
            "|",
            ("lot_id", "in", self.lot_id.ids),
            ("lot_id", "=", None),
            "|",
            ("stock_inventory_ids", "in", inventory_ids.ids),
            ("stock_inventory_ids", "=", None),
        ]

        quants = self.search(domain)

        products = self.env["product.product"]
        stock_inventory = self.env["stock.inventory"]

        for quant in quants:
            products |= quant.product_id
            stock_inventory |= quant.stock_inventory_ids

        stock_inventory = stock_inventory.filtered(lambda s: s.state == "in_progress")

        union_stock = stock_inventory & inventory_ids

        product_names = ", ".join([p.display_name for p in products])

        union_stock_names = ", ".join([u.name for u in union_stock])

        if quants:
            raise UserError(
                _(
                    'There are already adjustments open for products "{prod}" in '
                    '"{union}", you should rather modify this one instead of creating '
                    "a new one."
                ).format(prod=product_names, union=union_stock_names)
            )
