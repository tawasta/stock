from odoo import fields, models


class StockLocation(models.Model):

    _inherit = "stock.location"

    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Analytic account",
        help="Belongs to an analytic account",
    )
