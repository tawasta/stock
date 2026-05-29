from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    force_left_align_picking_report = fields.Boolean(
        string="Left-align Picking report headings",
        config_parameter="stock_report_force_left_align_headings.picking_enabled",
        default=True,
    )
    force_left_align_delivery_report = fields.Boolean(
        string="Left-align Delivery Slip headings",
        config_parameter="stock_report_force_left_align_headings.delivery_enabled",
        default=True,
    )
