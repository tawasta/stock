from datetime import datetime, timedelta

from odoo import fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    def _compute_last_modified_time(self):
        for lot in self:
            ir_config_model = self.env["ir.config_parameter"]
            modified_time_filter = (
                ir_config_model.sudo().get_param("modified_time_filter") or False
            )

            if modified_time_filter and modified_time_filter.isdigit():
                last_update = datetime.now() - lot.write_date
                last_update = (
                    last_update
                    and last_update < timedelta(hours=int(modified_time_filter))
                    and True
                ) or False
                lot.last_modified_time = last_update
            else:
                last_update = datetime.now() - lot.write_date
                last_update = (
                    last_update and last_update < timedelta(hours=24) and True
                ) or False
                lot.last_modified_time = last_update

    def _search_last_modified_time(self, operator, value):
        ir_config_model = self.env["ir.config_parameter"]
        modified_time_filter = (
            ir_config_model.sudo().get_param("modified_time_filter") or False
        )

        if modified_time_filter and modified_time_filter.isdigit():
            lots = self.env["stock.lot"].search(
                [
                    (
                        "write_date",
                        ">",
                        datetime.now() - timedelta(hours=int(modified_time_filter)),
                    )
                ]
            )
        else:
            lots = self.env["stock.lot"].search(
                [("write_date", ">", datetime.now() - timedelta(hours=24))]
            )
        return [("id", "in", lots.ids)]

    last_modified_time = fields.Boolean(
        compute="_compute_last_modified_time", search="_search_last_modified_time"
    )
