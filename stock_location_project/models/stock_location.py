# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockLocation(models.Model):

    _inherit = 'stock.location'

    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project',
        help='Belongs to a project'
    )
