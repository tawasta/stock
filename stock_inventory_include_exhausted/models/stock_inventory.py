from odoo import fields, models, _
from odoo.exceptions import ValidationError
from odoo.osv import expression

import logging

_logger = logging.getLogger(__name__)


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    include_exhausted = fields.Boolean(
        string="Include Exhausted",
        help="Create inventory rows also for exhausted products",
    )

    def _create_zero_quantity_quant(self, product, location):
        # Create a single stock.quant with a quantity of zero
        self.ensure_one()

        stock_quant_obj = self.env["stock.quant"]

        res = stock_quant_obj.create(
            {
                "current_inventory_id": self.id,
                "product_id": product.id,
                "location_id": location.id,
                "quantity": 0,
                "to_do": True,
                "user_id": self.responsible_id,
                "inventory_date": self.date,
            }
        )

        return res

    def _get_products_product_selection_manual(self):
        # Products when Product Selection = Manual Selection or One Product
        self.ensure_one()
        return self.product_ids

    def _get_products_product_selection_category(self):
        # Products when Product Selection = Product Category

        self.ensure_one()
        product_obj = self.env["product.product"]

        domain = [
            "|",
            ("categ_id", "=", self.category_id.id),
            ("categ_id", "in", self.category_id.child_id.ids),
        ]

        domain = expression.AND([domain, [("type", "=", "product")]])

        return product_obj.search(domain)

    def _get_products_product_selection_all(self):
        # Products when Product Selection = All Products
        self.ensure_one()

        product_obj = self.env["product.product"]

        domain = [("type", "=", "product")]

        return product_obj.search(domain)

    def action_state_to_in_progress(self):
        # Currently prevents using the exhausted option for multiple locations
        # and for lots, until support is implemented
        self.ensure_one()

        if self.include_exhausted:
            if len(self.location_ids) > 1:
                raise ValidationError(
                    _(
                        "'Include Exhausted' cannot be used when multiple locations are selected"
                    )
                )

            if self.product_selection == "lot":
                raise ValidationError(
                    _(
                        "'Include Exhausted' cannot be used when Product Selection is set to 'Lot/Serial Number'"
                    )
                )

        return super().action_state_to_in_progress()

    def action_view_inventory_adjustment(self):
        # Build quants for exhausted products. This needs to be done at this stage,
        # since core's _unlink_zero_quants() would delete any pre-built quants.

        res = super().action_view_inventory_adjustment()

        if self.include_exhausted:
            current_stock_quants = self._get_quants(self.location_ids)

            # stock_quant_obj = self.env["stock.quant"]

            # _logger.info("default quants:")
            # _logger.info(self._get_quants(self.location_ids))

            # _logger.info("quants before:")
            # _logger.info(len(self.stock_quant_ids))

            # Currently only a single location is supported
            location = self.location_ids[0]

            new_zero_stock_quant_ids = []

            # Form the list of products based on Product Selection.

            # One Product or Manual Selection
            if self.product_selection in ["manual", "one"]:
                products = self._get_products_product_selection_manual()

            # Product Category
            elif self.product_selection == "category":
                products = self._get_products_product_selection_category()

            # All Products
            elif self.product_selection == "all":
                products = self._get_products_product_selection_all()

            # TODO: add support for product_selection "lot". Currently forbidden
            # to begin adjustments with it

            for product in products:
                # For products that do not yet have a stock.quant, a new zero one
                # will be created
                if product.id not in [sq.product_id.id for sq in current_stock_quants]:
                    new_stock_quant_id = self._create_zero_quantity_quant(
                        product=product, location=location
                    )

                    new_zero_stock_quant_ids.append(new_stock_quant_id.id)
                    _logger.debug(
                        "Product %s did not yet have a quant, adding a zero quantity quant for it"
                        % product.product_tmpl_id.name
                    )
                else:
                    _logger.debug(
                        "Product %s already had a quant." % product.product_tmpl_id.name
                    )

            # Update the domain with the fresh contents of stock_quant_ids field
            self.refresh_stock_quant_ids()
            res["domain"] = [
                ("id", "in", self.stock_quant_ids.ids),
                ("current_inventory_id", "=", self.id),
            ]

        return res
