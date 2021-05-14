from odoo import fields
from odoo import models


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    invoiced_stock_picking_ids = fields.One2many(
        comodel_name="stock.picking",
        inverse_name="invoice_id",
        string="Invoiced pickings",
    )
