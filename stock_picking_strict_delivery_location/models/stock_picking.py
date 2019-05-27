from odoo import api, models


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    @api.onchange('picking_type_id', 'partner_id')
    def onchange_picking_type(self):
        super(StockPicking, self).onchange_picking_type()

        # Default domain
        field_domain = [('usage', '!=', 'view')]

        if self.partner_id:
            partner_location_id = self.partner_id.property_stock_customer

            if self.picking_type_id and \
                    self.picking_type_id.code == 'outgoing':

                if partner_location_id:
                    # Pre-set source and destination
                    if self.location_id.usage == 'customer':
                        self.location_id = partner_location_id

                    if self.location_dest_id.usage == 'customer':
                        self.location_dest_id = partner_location_id

                # Update domain:
                # only allow destinations belonging to the customer
                field_domain.append(
                    ('partner_id', '=', self.partner_id.id)
                )

        domain = {'domain': {'location_dest_id': field_domain}}

        return domain
