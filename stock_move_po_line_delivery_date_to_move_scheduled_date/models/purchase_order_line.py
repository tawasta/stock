from dateutil.relativedelta import relativedelta

from odoo import fields, models


class PurchaseOrderLine(models.Model):

    _inherit = "purchase.order.line"

    def write(self, values):
        for _line in self.filtered(lambda l: not l.display_type):
            if values.get("date_planned"):
                new_date = fields.Datetime.to_datetime(values["date_planned"])
                self._update_move_scheduled_date(new_date)
        return super().write(values)

    def _update_move_scheduled_date(self, new_date):
        """Sets Scheduled Date to be the same as Deadline"""
        moves_to_update = self.move_ids.filtered(
            lambda m: m.state not in ("done", "cancel")
        )
        if not moves_to_update:
            moves_to_update = self.move_dest_ids.filtered(
                lambda m: m.state not in ("done", "cancel")
            )
        for move in moves_to_update:
            move.date = new_date + relativedelta(days=move.company_id.po_lead)
