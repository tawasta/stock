from odoo import fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    invoice_id = fields.Many2one(
        string="Invoice",
        comodel_name="account.invoice",
        help="Related invoice",
        copy=False,
        readonly=True,
    )
