from odoo import fields, models


class ResCompany(models.Model):

    _inherit = 'res.company'

    stock_update_qty_location_default = fields.Many2one(
        comodel_name='stock.location',
        domain=[('usage', '=', 'internal')],
        string='Default stock qty update location',
        help="Suggested as a default when updating a product's quantity",
    )
