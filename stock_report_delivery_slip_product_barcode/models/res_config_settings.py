from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    delivery_slip_product_barcodes = fields.Boolean(
        readonly=False,
        store=True,
        config_parameter="stock_report_delivery_slip_product_barcodes.delivery_slip_product_barcodes",
    )
