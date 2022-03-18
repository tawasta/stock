from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockMove(models.Model):

    _inherit = "stock.move"

    def _compute_product_bom_ids(self):
        for move in self:
            if move.product_id.bom_ids:
                move.has_bom = True

    has_bom = fields.Boolean(string="BoMs", compute="_compute_product_bom_ids")
    manufacturing_order_id = fields.Many2one(comodel_name="mrp.production", copy=False)
    mo_state = fields.Selection(related="manufacturing_order_id.state", copy=False)
    mo_has_been_created = fields.Boolean(
        string="MO has been created", default=False, copy=False
    )
    mo_to_complete = fields.Boolean(string="Complete the MO", default=True, copy=False)

    def create_and_validate_manufacturing_order(self):
        if not self.manufacturing_order_id:
            self.create_manufacturing_order()
        self.validate_manufacturing_order()

    def create_manufacturing_order(self):
        self.ensure_one()
        manufacturing_order = self.env["mrp.production"]

        product = self.product_id
        bom = product.bom_ids and product.bom_ids[0] or False

        picking_type_id = (
            self.env["stock.warehouse"]
            .search([("company_id", "=", self.company_id.id)], limit=1)
            .manu_type_id.id
        )

        # Subtracts the difference between reserved and ordered quantity
        ml_qty = self.move_line_ids and self.move_line_ids[0].product_uom_qty or 0
        qty_to_produce = self.product_uom_qty - ml_qty

        if bom:
            values = {
                "origin": self.picking_id.name,
                "product_id": product.id,
                "product_qty": qty_to_produce,
                "product_uom_id": self.product_uom.id,
                "bom_id": bom.id,
                "date_planned_start": fields.Datetime.now(),
                "company_id": self.company_id.id,
                "location_src_id": self.location_id.id,
                "location_dest_id": self.location_id.id,
                "picking_type_id": picking_type_id,
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
                Please refresh the page."""
                % mo.name
            )
            if mo.state == "done":
                raise UserError(msg_done)

            mo.action_assign()
            if mo.state == "confirmed" and mo.availability in [
                "assigned",
                "partially_available",
                "waiting",
            ]:
                mo.button_plan_start_work_orders()
            if mo.state == "progress":
                mo.button_mark_done()
                self.mo_to_complete = False

        # Check quantities which can be reserved
        self.picking_id.action_assign()
