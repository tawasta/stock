from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    location_name_report_style = fields.Selection(
        [
            ("full", "Full Path"),
            ("short", "Short Name"),
        ],
        default="full",
        help=(
            "Choose whether location names in printed reports and barcode labels "
            "display the full hierarchical path (e.g. WH/Stock/Shelf A) or the short "
            "name (e.g. Shelf A)."
        ),
    )
