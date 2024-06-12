from odoo import api, fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    delay = fields.Integer(string="Delay", compute="_compute_delay", store=True)

    @api.depends("scheduled_date", "date_done")
    def _compute_delay(self):
        for record in self:
            if record.scheduled_date and record.date_done:
                delta = record.date_done - record.scheduled_date
                # Calulate the delay in days
                delay_days = delta.days + delta.seconds / (24 * 3600)
                record.delay = round(delay_days)
            else:
                record.delay = False
