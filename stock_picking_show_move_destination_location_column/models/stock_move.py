from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    dest_location_domain_ids = fields.Many2many(
        "stock.location", related="location_dest_id.child_internal_location_ids"
    )
