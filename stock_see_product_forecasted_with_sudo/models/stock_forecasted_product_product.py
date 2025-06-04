import logging

from odoo import models

_logger = logging.getLogger(__name__)


class StockForecasted(models.AbstractModel):
    _inherit = "stock.forecasted_product_product"

    def _get_report_data(self, product_template_ids=False, product_ids=False):
        """Rewritten function with sudo rights"""
        assert product_template_ids or product_ids
        res = {}

        if self.env.context.get("warehouse") and isinstance(
            self.env.context["warehouse"], int
        ):
            warehouse = (
                self.env["stock.warehouse"]
                .sudo()
                .browse(self.env.context.get("warehouse"))
            )
        else:
            warehouse = (
                self.env["stock.warehouse"].sudo().search([["active", "=", True]])[0]
            )

        wh_location_ids = [
            loc["id"]
            for loc in self.env["stock.location"].search_read(
                [("id", "child_of", warehouse.view_location_id.id)],
                ["id"],
            )
        ]
        # any quantities in this location will be considered free stock, others are free stock in transit
        wh_stock_location = warehouse.lot_stock_id

        res.update(
            self._get_report_header(product_template_ids, product_ids, wh_location_ids)
        )

        res["lines"] = self.sudo()._get_report_lines(
            product_template_ids, product_ids, wh_location_ids, wh_stock_location
        )
        return res
