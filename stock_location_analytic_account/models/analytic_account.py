# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo import exceptions


class AnalyticAccount(models.Model):

    _inherit = 'account.analytic.account'

    location_ids = fields.One2many(
        comodel_name='stock.location',
        inverse_name='analytic_account_id',
        string='Inventory locations',
    )
    default_location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Default location',
        default=lambda self: self._default_get_default_location(),
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
                'location_id': warehouse.lot_stock_id.id,
            }
            location = self.env['stock.location'].create(location_values)

            # Create a new location
            values['default_location_id'] = location.id
            values['location_ids'] = [(6, False, [location.id])]

        return super(AnalyticAccount, self).create(values)

    @api.onchange('location_ids')
    @api.depends('location_ids')
    def _default_get_default_location(self):
        for record in self:
            if record.location_ids and not record.default_location_id:
                record.default_location_id = record.location_ids[0]

    @api.constrains('default_location_id')
    def _validate_default_location_id(self):
        if self.location_ids and \
                        self.default_location_id not in self.location_ids:
            msg = _('Please use a location in the inventory locations.')
            raise exceptions.ValidationError(msg)