# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.tools.translate import _


class StockMove(models.Model):

    _inherit = 'stock.move'

    @api.multi
    @api.depends('date_expected')
    def _compute_date_expected_postponed(self):
        for move in self:
            if move.date_expected > move.date_expected_original:
                move.date_expected_postponed = True
            else:
                move.date_expected_postponed = False

    @api.model
    def create(self, values):
        res = super(StockMove, self).create(values)
        res.date_expected_original = res.date_expected
        return res

    date_expected_postponed = fields.Boolean(
        string='Date Expected Postponed',
        compute=_compute_date_expected_postponed,
        store=True
    )

    date_expected_original = fields.Datetime(
        string='Date Originally Expected',
        help='Date that was originally given to the move at creation'
    )
