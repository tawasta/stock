
from odoo import api, fields, models


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    force_unreserve = fields.Boolean(string="Force Unreserve",
            default=lambda self: self._default_force_unreserve())

    @api.model
    def create(self, vals):
        backorder = vals.get('backorder_id', False)
        if backorder:
            vals['force_unreserve'] = True

        return super().create(vals)

    def _default_force_unreserve(self):
        if self.sale_id:
            return self.env.user.company_id.force_unreserve
        else:
            return False

    @api.multi
    def action_assign(self):
        """ Conditions for reservation. A delivery is not reserved if its
            sale order had force_unreserve set as True """
        for picking in self:
            backorder = picking.backorder_id

            backorder_force = backorder and backorder.force_unreserve or False

            if picking.group_id.sale_id and picking.group_id.force_unreserve or\
                    picking.force_unreserve:

                # Backorder's force_unreserve field is set to False
                # which means that this order can now be reserved
                if backorder_force:
                    backorder.force_unreserve = False
                picking.group_id.force_unreserve = False

                if backorder and all([move for move
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
