# -*- coding: utf-8 -*-
from odoo import models, api


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):
        # Add serial numbers to invoice description
        for record in self:
            for invoice_line in record.invoice_line_ids:
                description = ""

        return super(AccountInvoice, self).action_invoice_open()
