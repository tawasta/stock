# -*- coding: utf-8 -*-
from odoo import models, api, _


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):
        # Add picking names to invoice description
        for record in self:
            if record.picking_ids:
                description = record.comment or ''
                description += _("Invoiced deliveries: ")

                for picking in record.picking_ids:
                    description += "\n%s" % picking.name

                record.comment = description

        return super(AccountInvoice, self).action_invoice_open()
