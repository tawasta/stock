from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    stock_report_delivery_slip_c5_vertical_offset = fields.Float(
        string="Delivery Slip: C5 Letter Vertical Offset (mm)",
        help="Adjust as needed to get the print's address to align with the "
        "C5 letter's window. Positive values move the address down, "
        "negative values up.",
        config_parameter=(
            "stock_report_delivery_slip_c5_letter_friendly_positioning.vertical_offset"
        ),
    )

    stock_report_delivery_slip_c5_horizontal_offset = fields.Float(
        string="Delivery Slip: C5 Letter Horizontal Offset (mm)",
        help="Adjust as needed to get the print's address to align with the "
        "C5 letter's window. Positive values move the address right, "
        "negative values left.",
        config_parameter=(
            "stock_report_delivery_slip_c5_letter_friendly_positioning"
            ".horizontal_offset"
        ),
    )
