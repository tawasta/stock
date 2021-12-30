from odoo import fields
from odoo import models


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    active = fields.Boolean(
        default=True,
    )

    def toggle_active(self):
        """ Archiving valuation layer record will set any related account moves to draft """
        result = super().toggle_active()

        for record in self:
            if record.account_move_id:
                if not record.active and record.account_move_id.state == "posted":
                    record.account_move_id.button_draft()
                elif record.active and record.account_move_id.state == "draft":
                    record.account_move_id.action_post()

        return result
