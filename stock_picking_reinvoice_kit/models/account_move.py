from odoo import fields, models


class AccountMove(models.Model):

    _inherit = "account.move"

    invoiced_stock_picking_ids = fields.One2many(
        comodel_name="stock.picking",
        inverse_name="invoice_id",
        string="Invoiced pickings",
    )
