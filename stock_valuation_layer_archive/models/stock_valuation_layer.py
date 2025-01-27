from odoo import fields, models


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    active = fields.Boolean(
        default=True,
    )

    def toggle_active(self):
        """Archiving valuation layer record will set any related account moves to draft"""
        result = super().toggle_active()

        for record in self:
            if record.account_move_id:
                if not record.active and record.account_move_id.state == "posted":
                    record.account_move_id.button_draft()
                    record.account_move_id.button_cancel()
                elif record.active and record.account_move_id.state == "cancel":
                    record.account_move_id.button_draft()
                    record.account_move_id.action_post()

        return result
