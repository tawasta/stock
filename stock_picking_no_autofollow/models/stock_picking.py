from odoo import api, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    @api.model
    def create(self, vals):
        res = super().create(vals)

        for record in res:
            # We can't prevent the subscription, so we'll just
            # unsubscribe right after creating
            if record.partner_id in record.message_partner_ids:
                record.message_unsubscribe([record.partner_id.id])

        return res

    def write(self, vals):
        res = super().write(vals)

        for record in self:
            # We can't prevent the subscription, so we'll just
            # unsubscribe right after writing
            if record.partner_id in record.message_partner_ids:
                record.message_unsubscribe([record.partner_id.id])

        return res
