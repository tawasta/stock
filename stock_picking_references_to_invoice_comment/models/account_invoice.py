from odoo import _, models


class AccountMove(models.Model):

    _inherit = "account.move"

    def action_post(self):
        # Add picking names to invoice description
        for record in self:
            if record.picking_ids:
                description = record.narration or ""
                description += _("Invoiced deliveries: ")

                for picking in record.picking_ids:
                    description += "\n%s" % picking.name

                record.narration = description

        return super().action_post()
