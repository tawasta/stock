# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockInventoryLine(models.Model):

    _inherit = 'stock.inventory.line'

    price_unit = fields.Float(
        string='Unit Price',
        help='Technical field used to set the product quant cost',
        # The digits-attribute is not provided,
        # as the stock.move price_unit won't have it either
    )

    @api.onchange('product_id')
    @api.depends('product_id')
    def onchange_product_id_update_cost(self):
        for record in self:
            if record.product_id:
                record.price_unit = record.product_id.standard_price

    def _generate_moves(self):
        return super(StockInventoryLine, self)._generate_moves()

    @api.model
    def create(self, vals):
        # Set the product price
        if vals.get('product_id', False):
            product = self.env['product.product'].search([
                ('id', '=', vals.get('product_id'))
            ])

            vals['price_unit'] = product.standard_price

        return super(StockInventoryLine, self).create(vals)

    def _get_move_values(self, qty, location_id, location_dest_id):
        # Add manual cost price to lines

        res = super(StockInventoryLine, self)._get_move_values(
            qty=qty,
            location_id=location_id,
            location_dest_id=location_dest_id
        )

        res['price_unit'] = self.price_unit

        return res
