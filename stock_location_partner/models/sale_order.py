# -*- coding: utf-8 -*-
from odoo import models, api


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        # If partner doesn't have own location, create one
        StockLocation = self.env['stock.location']

        # TODO: allow choosing a default location, if partner has many
        customer_location = StockLocation.search([
            ('partner_id', '=', self.partner_shipping_id.id),
            ('company_id', '=', self.company_id.id),
            ('usage', '=', 'customer'),
        ], limit=1)

        if not customer_location:
            default_location = self.env.ref('stock.stock_location_customers')

            location_values = {
                'name': self.partner_shipping_id.name,
                'usage': 'customer',
                'location_id': default_location.id,
                'company_id': self.company_id.id,
                'partner_id': self.partner_shipping_id.id,
            }

            customer_location = StockLocation.create(location_values)

            # Don't overwrite a custom location
            if self.partner_shipping_id.property_stock_customer \
                    == default_location:
                self.partner_shipping_id.property_stock_customer \
                    = customer_location

        return super(SaleOrder, self).action_confirm()
