# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    location_ids = fields.One2many(
        comodel_name='stock.location',
        inverse_name='analytic_account_id',
        string='Inventory locations',
    )
