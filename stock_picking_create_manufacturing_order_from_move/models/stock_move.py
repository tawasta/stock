from odoo import _, fields, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    def _compute_product_bom_ids(self):
        """has_bom value determines if 'Product product' button is shown"""
        for move in self:
            if move.product_id and move.product_id.bom_ids:
                move.has_bom = True
            else:
                move.has_bom = False

    has_bom = fields.Boolean(
        string="BoMs", compute=lambda self: self._compute_product_bom_ids()
    )
    manufacturing_order_id = fields.Many2one(comodel_name="mrp.production", copy=False)
    mo_state = fields.Selection(related="manufacturing_order_id.state", copy=False)
    mo_has_been_created = fields.Boolean(
        string="MO has been created", default=False, copy=False
    )

    def create_and_validate_manufacturing_order(self):
        """Create and validate a new manufacturing order"""
        qty_to_produce = self.product_uom_qty
        # Return a pop-up window if a quantity to be produced is zero.
        if qty_to_produce == 0:
            msg = _(
                "Manufacturing Order was not created, because there is "
                "enough in stock of this product."
            )
            message = self.env["stock.move.create.manufacturing.order.message"].create(
                {"mo_message": msg}
            )

            return {
                "type": "ir.actions.act_window",
                "res_model": "stock.move.create.manufacturing.order.message",
                "view_type": "form",
                "view_mode": "form",
                "res_id": message.id,
                "target": "new",
            }

        if not self.manufacturing_order_id:
            self.create_manufacturing_order()
        self.validate_manufacturing_order()

    def create_manufacturing_order(self):
        """Create a new manufacturing order from Stock Move"""
        self.ensure_one()

        manufacturing_order_model = self.env["mrp.production"]

        product = self.product_id
        bom = product.bom_ids and product.bom_ids[0] or False

        picking_type_id = (
            self.env["stock.warehouse"]
            .search([("company_id", "=", self.env.user.company_id.id)], limit=1)
            .manu_type_id.id
        )

        qty_to_produce = self.product_uom_qty

        if bom:
            # Assign values
            values = {
                "origin": self.picking_id.name,
                "product_id": product.id,
                "product_qty": qty_to_produce,
                "product_uom_id": self.product_uom.id,
                "bom_id": bom.id,
                "date_start": fields.Datetime.now(),
                "company_id": self.env.user.company_id.id,
                "location_src_id": self.location_id.id,
                "location_dest_id": self.location_id.id,
                "picking_type_id": picking_type_id,
            }

            prod = manufacturing_order_model.create(values)
            self.manufacturing_order_id = prod

            prod._plan_workorders()

            self.mo_has_been_created = True
            return prod
        else:
            return None

    def validate_manufacturing_order(self):
        """Validate Stock Move's production order"""
        mo = self.manufacturing_order_id

        if mo:
            msg_done = _(
                """The Manufacturing Order %s has already been marked as Done.
                Please refresh the page."""
                % mo.name
            )
            # Raise an UserError if a production order is already done.
            if mo.state == "done":
                raise UserError(msg_done)
            mo.action_confirm()
            mo.button_plan()
            mo.button_mark_done()

        # Check quantities which can be reserved
        self._action_assign()
        self.move_has_been_reserved = True
