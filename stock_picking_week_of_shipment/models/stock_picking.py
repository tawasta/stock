from odoo import fields, models, api
from datetime import datetime, date, timedelta


class SaleOrder(models.Model):

    _inherit = "stock.picking"

    week_of_shipment = fields.Integer(
        string="Week of shipment",
        readonly=False,
        store=True
    )

    @api.depends("date_done")
    @api.onchange("date_done")
    def _compute_week_of_shipment(self):
        for record in self:
            if record.date_done:
                week_from_date = date(
                    record.date_done.year,
                    record.date_done.month,
                    record.date_done.day
                ).isocalendar()[1]
                if week_from_date != record.week_of_shipment:
                    record.week_of_shipment = week_from_date

    @api.depends("week_of_shipment")
    @api.onchange("week_of_shipment")
    def _compute_date_done(self):
        for record in self:
            week_from_date = 0
            if record.date_done:
                week_from_date = date(
                    record.date_done.year,
                    record.date_done.month,
                    record.date_done.day
                ).isocalendar()[1]

            if record.week_of_shipment > 0 and record.week_of_shipment < 53:
                if week_from_date != record.week_of_shipment:
                    weeks = record.week_of_shipment
                    days_in_week = 7
                    nth_day = weeks * days_in_week - days_in_week
                    current_year = datetime.now().year
                    start_of_year = datetime(current_year, 1, 1)
                    record.date_done = start_of_year + timedelta(days=nth_day)
            else:
                self._compute_week_of_shipment()
