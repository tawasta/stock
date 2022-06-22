from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    stock_report_decimal_precision = fields.Integer(
        related="company_id.stock_report_decimal_precision",
        readonly=False,
    )

    @api.onchange("stock_report_decimal_precision")
    def onchange_stock_report_decimal_precision(self):
        company_precision = self.env.ref(
            "stock_report_quantity_decimals.decimal_company_precision"
        )

        company_precision.digits = self.stock_report_decimal_precision
