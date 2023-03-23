from odoo import fields, models, api


class Picking(models.Model):

    _inherit = "stock.picking"

    stock_scheduled_date = fields.Datetime(
        'Scheduled Date',  store=True,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        related='scheduled_date')


