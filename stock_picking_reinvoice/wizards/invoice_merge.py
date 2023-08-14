from odoo import models


class InvoiceMerge(models.TransientModel):
    _inherit = "invoice.merge"

    def merge_invoices(self):
        inv_obj = self.env["account.move"]
        old_ids = self.env.context.get("active_ids", [])
        old_invoices = inv_obj.browse(old_ids)
        res = super().merge_invoices()
        # Get new invoice from result
        invoice_domain = res.get("domain")
        all_ids = invoice_domain[0][2]
        new_invoice = [value for value in all_ids if value not in old_ids]

        # Update old invoice pickings invoice link
        for old_invoice in old_invoices:
            if old_invoice.invoiced_stock_picking_ids:
                old_invoice.invoiced_stock_picking_ids.write(
                    {"invoice_id": new_invoice[0]}
                )
                # Unlink old invoices to avoid having lots of cancelled junk
                old_invoice.unlink()
