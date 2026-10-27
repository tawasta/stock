from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    stock_putaway_default_location = fields.Many2one(
        comodel_name="stock.location",
        string="Default putaway arrive location",
        help="""For default product location, select a default arrive
        location in Putaway rules""",
    )
