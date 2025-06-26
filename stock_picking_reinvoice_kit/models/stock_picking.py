from odoo import fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    invoice_id = fields.Many2one(
        string="Invoice",
        comodel_name="account.move",
        help="Related invoice",
        copy=False,
        readonly=True,
    )

    invoice_state = fields.Selection(
        string="Invoice Status",
        related="invoice_id.state",
    )
