# -*- coding: utf-8 -*-
from odoo import models, fields


class StockLocation(models.Model):

    _inherit = 'stock.location'

    tag_ids = fields.Many2many(
        related='analytic_account_id.tag_ids',
        string='Tags'
    )
