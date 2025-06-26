from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockPickingInvoiceWizard(models.TransientModel):

    _inherit = "stock.picking.invoice.wizard"

    invoice_kit = fields.Boolean(string="Invoice kits", default=False)

    def action_create_invoice(self):
        # TODO: break down the original function to allow inheritance

        invoice, picking_ids = super().action_create_invoice()

        # TODO: If "invoice_kit" is selected,
        #  go through picking_ids and group them by sales package,
        #  instead of products
        if self.invoice_kit:
            raise Exception("Invoicing by kits is not implemented")

        return invoice, picking_ids
