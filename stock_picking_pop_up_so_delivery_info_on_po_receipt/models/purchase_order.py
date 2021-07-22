# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    @api.depends('order_line.procurement_ids')
    def _compute_created_form_sale_order(self):
        for order in self:
            for line in order.order_line:
                if [p.sale_line_id for p in line.procurement_ids]:
                    order.created_from_sale_order = True

    created_from_sale_order = fields.Boolean(
        compute="_compute_created_form_sale_order")
