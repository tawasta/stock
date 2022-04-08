
from odoo import api, fields, models


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    force_unreserve = fields.Boolean(string="Force Unreserve", default=False)

    @api.multi
    def action_assign(self):
        """ Conditions for reservation. A delivery is not reserved if its
            sale order had force_unreserve set as True """
        for picking in self:

            backorder_force = picking.backorder_id and\
                    picking.backorder_id.force_unreserve or False

            # Check does a delivery have a backorder
            if picking.group_id.sale_id and picking.group_id.force_unreserve or\
                    backorder_force:

                # Backorder's force_unreserve field is set to False
                # which means that this order can now be reserved
                if backorder_force:
                    picking.backorder_id.force_unreserve = False
                picking.group_id.force_unreserve = False

                if picking.backorder_id and all([move for move
                        in picking.move_lines if move.reserved_availability == 0]):
                    picking.do_unreserve()

                return True
            else:
                if picking.group_id.sale_id:
                    picking.force_unreserve = True
                super(StockPicking, picking).action_assign()

    @api.multi
    def do_unreserve(self):
        """ A small change so that the action_assign button will
            not be needed to be pushed twice """
        for picking in self:
            # Check if a delivery is from sale order, just in case
            if picking.group_id.sale_id and picking.group_id.force_unreserve:
                picking.group_id.force_unreserve = False
            picking.force_unreserve = False
            super(StockPicking, picking).do_unreserve()

    @api.multi
    def action_cancel(self):
        """ In case a sale order is canceled and confirmed again, it is
            necessary to set a procurement group's force_unreserve-field
            to True. This way the sale order's new transfer will not be
            reserved. """
        for picking in self:
            picking.group_id.force_unreserve = True
            return super(StockPicking, picking).action_cancel()
