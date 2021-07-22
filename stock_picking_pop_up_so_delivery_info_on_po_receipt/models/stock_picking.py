# -*- coding: utf-8 -*-
from odoo import fields, models, _


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    warning_helper = fields.Boolean(
        related='purchase_id.created_from_sale_order')

    def show_warning_if_picking_has_so_and_po(self):
        message = _("""
            A sale order delivery is linked to this Receipt.
            Remember to finish that delivery.
        """)

        view = self.env.ref(
            'stock_picking_pop_up_so_delivery_info_on_po_receipt.'
            'stock_picking_wizard_po_warning')
        wiz = self.env['stock.picking.sale.order.warning'].sudo().create(
            {'text': message, 'picking_id': self.id})

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking.sale.order.warning',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': view.id,
            'res_id': wiz.id,
            'target': 'new',
        }
