# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProjectProject(models.Model):

    _inherit = 'project.project'

    location_ids = fields.One2many(
        comodel_name='stock.location',
        inverse_name='project_id',
        string='Inventory locations',
    )

    @api.model
    def create(self, values):
        if 'location_ids' not in values or not values['location_ids']:
            # Auto-generate a stock location
            warehouse_model = self.env['stock.warehouse']
            stock_location_model = self.env['stock.location']

            # Get the first warehouse
            # TODO: allow selecting the default warehouse
            warehouse = warehouse_model.search([], limit=1)

            location_values = {
                'name': values['name'],
                'usage': 'internal',
                'location_id': warehouse.view_location_id.id,
            }

            # Create a new location
            values['location_ids'] = [(0, False, location_values)]

        return super(ProjectProject, self).create(values)