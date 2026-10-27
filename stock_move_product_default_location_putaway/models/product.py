import logging

from odoo import models

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def write(self, values):
        """Change putaway arrive location to the new default location if
        the old arrive location matches with the old product default location."""
        company_id = self.env.company
        company_default_putaway_location = company_id.stock_putaway_default_location
        new_default_location_id = values.get("default_stock_move_location_id", False)
        new_default_location = (
            new_default_location_id
            and self.env["stock.location"].browse(new_default_location_id)
            or False
        )

        if new_default_location and company_default_putaway_location:
            variants = self.product_variant_ids
            putaway_rule = self.env["stock.putaway.rule"]
            # Checks if the old default location is the same as what it used
            # in putaway rule
            for variant in variants:
                putaway_rule |= self.env["stock.putaway.rule"].search(
                    [
                        ("product_id", "=", variant.id),
                        ("location_in_id", "=", company_default_putaway_location.id),
                    ]
                )
            if putaway_rule:
                putaway_rule.location_out_id = new_default_location
            else:
                created_ids = self.env["stock.putaway.rule"]
                for variant in variants:
                    putaway_values = {
                        "product_id": variant.id,
                        "location_in_id": company_default_putaway_location.id,
                        "location_out_id": new_default_location.id,
                    }

                    created_ids |= self.env["stock.putaway.rule"].create(putaway_values)
                    _logger.info(
                        "Created Putaway rules with product write: "
                        f"{created_ids.ids}"
                    )

        res = super().write(values)
        return res

    def cron_product_default_location_putaway(self):
        """Change putaway arrive location to the new default location if
        the old arrive location matches with the old product default location."""
        products = self.env["product.template"].search(
            [("default_stock_move_location_id", "!=", False)]
        )

        for product in products:
            company_id = self.env.company
            company_default_putaway_location = company_id.stock_putaway_default_location
            new_default_location = product.default_stock_move_location_id

            if new_default_location and company_default_putaway_location:
                variants = product.product_variant_ids
                putaway_rule = self.env["stock.putaway.rule"]
                # Checks if the old default location is the same as what it used
                # in putaway rule
                for variant in variants:
                    putaway_rule |= self.env["stock.putaway.rule"].search(
                        [
                            ("product_id", "=", variant.id),
                            (
                                "location_in_id",
                                "=",
                                company_default_putaway_location.id,
                            ),
                        ]
                    )
                if putaway_rule:
                    putaway_rule.location_out_id = new_default_location
                else:
                    created_ids = self.env["stock.putaway.rule"]
                    for variant in variants:
                        putaway_values = {
                            "product_id": variant.id,
                            "location_in_id": company_default_putaway_location.id,
                            "location_out_id": new_default_location.id,
                        }

                        created_ids |= self.env["stock.putaway.rule"].create(
                            putaway_values
                        )
                        _logger.info(
                            "Created Putaway rules with scheduled action: "
                            f"{created_ids.ids}"
                        )
