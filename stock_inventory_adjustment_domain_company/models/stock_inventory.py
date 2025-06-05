from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    location_id = fields.Many2one(
        "stock.location",
        "Parent Location",
        index=True,
        ondelete="cascade",
        check_company=True,
        domain="[('company_id', 'in', [company_id, False]),"
        "('usage', 'in', ['internal', 'transit'])]",
        help="The parent location that includes this location. "
        "Example : The 'Dispatch Zone' is the 'Gate 1' parent location.",
    )
