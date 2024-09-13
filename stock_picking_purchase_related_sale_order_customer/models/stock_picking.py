from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    so_partner_id = fields.Many2one(related="purchase_id.so_partner_id")
