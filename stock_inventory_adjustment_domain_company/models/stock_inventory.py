from odoo import fields, models


class StockInventory(models.Model):

    _inherit = "stock.inventory"

    location_ids = fields.Many2many(
        "stock.location",
        domain="[('company_id', 'in', [company_id, False]),"
        "('usage', 'in', ['internal', 'transit'])]",
    )
