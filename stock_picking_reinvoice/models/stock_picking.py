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
        [
            ("draft", "Draft"),
            ("open", "Open"),
            ("in_payment", "In Payment"),
            ("paid", "Paid"),
            ("cancel", "Cancelled"),
        ],
        string="Invoice status",
        related="invoice_id.state",
    )
