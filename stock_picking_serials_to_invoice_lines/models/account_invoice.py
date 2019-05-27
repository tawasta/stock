from odoo import models, api, _


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):
        # Add picking serials to invoice lines
        for record in self:
            if record.invoice_line_ids:
                record._add_picking_serials_to_line_name()

        return super(AccountInvoice, self).action_invoice_open()

    def _add_picking_serials_to_line_name(self):
        self.ensure_one()

        if self.invoice_line_ids:
            description = self.comment or ''
            description += "\n" + _("Delivered serials/lots: ")

        for line in self.invoice_line_ids:
            for move in line.move_line_ids:
                for quant in move.quant_ids:
                    if quant.lot_id:
                        description += "\n%s" % quant.lot_id.name

        self.comment = description
