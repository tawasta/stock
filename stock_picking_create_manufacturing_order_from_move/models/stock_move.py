from odoo import fields, models, _
from odoo.exceptions import UserError


class StockMove(models.Model):

    _inherit = 'stock.move'

    def _compute_product_bom_ids(self):
        for move in self:
            if move.product_id.bom_ids:
                move.has_bom = True

    has_bom = fields.Boolean(string="BoMs", compute="_compute_product_bom_ids")
    manufacturing_order_id = fields.Many2one(comodel_name='mrp.production',
                                             copy=False)
    mo_state = fields.Selection(related="manufacturing_order_id.state",
                                copy=False)
    mo_has_been_created = fields.Boolean(string="MO has been created",
                                         default=False, copy=False)
    mo_to_complete = fields.Boolean(string="Complete the MO",
                                    default=False, copy=False)

    def create_manufacturing_order(self):
        self.ensure_one()
        manufacturing_order = self.env['mrp.production']

        product = self.product_id
        bom = product.bom_ids and product.bom_ids[0] or False

        if bom:
            values = {
                'origin': self.picking_id.name,
                'product_id': product.id,
                'product_qty': self.product_uom_qty,
                'product_uom_id': self.product_uom.id,
                'bom_id': bom.id,
                'date_planned_start': fields.Datetime.now(),
                'company_id': self.company_id.id,
                'location_src_id': self.location_id.id,
                'location_dest_id': self.location_id.id,
            }
            prod_order = manufacturing_order.create(values)
            self.manufacturing_order_id = prod_order.id
            self.mo_has_been_created = True
            self.mo_to_complete = True
            return prod_order
        else:
            return None

    def validate_manufacturing_order(self):
        mo = self.manufacturing_order_id

        if mo:
            msg_done = _(
                """The Manufacturing Order %s has already been marked as Done.
                Please refresh the page.""" % mo.name)
            if mo.state == 'done':
                raise UserError(msg_done)

#             msg_avail = _("Not enough materials to complete production order.")
#             if mo.availability in ['assigned', 'partially_available',
#                                    'waiting']:
#                 raise UserError(msg_avail)

            mo.action_assign()
            if mo.state == 'confirmed' and \
                    mo.availability in ['assigned', 'partially_available']:
                mo.button_plan()
            if mo.state == 'progress':
                mo.button_mark_done()
                self.mo_to_complete = False

        # Check quantities which can be reserved
        self.picking_id.action_assign()