# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    @api.multi
    @api.onchange('product_id')
    def onchange_product_id_route_warning(self):

        product = self.product_id

        if not product:
            return

        result = dict()

        for route in product.route_ids:
            if route.sale_line_warn != 'no-message':
                title = _("Warning for %s") % product.name
                message = route.sale_line_warn_msg

                warning = dict(
                    title=title,
                    message=message,
                )

                result = {'warning': warning}

            if route.sale_line_warn == 'block':
                self.product_id = False

        return result
