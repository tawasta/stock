from collections import defaultdict

from odoo import models
from odoo.exceptions import UserError

from odoo.addons.stock_account.models.stock_move import StockMove


# ruff: noqa: E501
def _set_value(self, correction_quantity=None):
    """A small modification to add percentage to stock valuation
    when an average price is used."""
    products_to_recompute = set()
    lots_to_recompute = set()
    fifo_qty_processed = defaultdict(float)

    for move in self:
        # Incoming moves
        if move.is_dropship or move.is_in:
            products_to_recompute.add(move.product_id.id)
            if move.product_id.lot_valuated:
                if any(not ml.lot_id for ml in move.move_line_ids):
                    raise UserError(
                        self.env._(
                            "A lot/serial number is required for product '%s' as it has lot valuation enabled.",
                            move.product_id.display_name,
                        )
                    )
                lots_to_recompute.update(move.move_line_ids.lot_id.ids)
        if move.is_in:
            move.value = move.sudo()._get_value()
            continue
        # Outgoing moves
        if not move._is_out():
            continue
        if correction_quantity:
            previous_qty = move.quantity - correction_quantity
            ratio = correction_quantity / previous_qty if previous_qty else 0
            move.value += ratio * move.value
            continue
        if move.product_id.lot_valuated:
            value = 0.0
            for move_line in move.move_line_ids:
                if move_line.lot_id:
                    value += (
                        move_line.lot_id.standard_price * move_line.quantity_product_uom
                    )
                else:
                    value += (
                        move.product_id.standard_price * move_line.quantity_product_uom
                    )
            move.value = value
            continue

        if move.product_id.cost_method == "fifo":
            valued_qty = move._get_valued_qty()
            move.value = move.product_id.with_context(
                fifo_qty_already_processed=fifo_qty_processed[move.product_id]
            )._run_fifo(valued_qty)
            fifo_qty_processed[move.product_id] += valued_qty
        else:
            #######################################################################
            # HERE IS THE CHANGED PART!
            # THIS ID DONE THIS WAY TO NOT MESS UP THE INHERITANCE OF OTHER MODULES
            #######################################################################
            product = move.product_id
            percentage = (
                product.categ_id and product.categ_id.percentage_update or False
            )
            if percentage and product.cost_method == "average":
                move.value = (
                    move.product_id.standard_price
                    * move._get_valued_qty()
                    * (1 + percentage)
                )
            else:
                move.value = move.product_id.standard_price * move._get_valued_qty()

    # Recompute the standard price
    self.env["product.product"].browse(products_to_recompute)._update_standard_price()
    self.env["stock.lot"].browse(lots_to_recompute)._update_standard_price()


# The original method is set to use the modified method with percentage change.
# This allows other modules to inherit the method, acting as it were the original
# method (function).
StockMove._set_value = _set_value


class StockMove(models.Model):
    _inherit = "stock.move"

    def _action_done(self, cancel_backorder=False):
        """Search received moves and add percentage update to the Cost of
        their products"""
        moves = super()._action_done(cancel_backorder=cancel_backorder)

        # We get the products the same way Odoo normally does to avoid possible issues
        moves_in = moves.filtered(lambda m: m.is_in or m.is_dropship)
        products_to_recompute = set()

        for move in moves_in:
            products_to_recompute.add(move.product_id.id)

        products = self.env["product.product"].browse(products_to_recompute)

        # Note that the Cost of a product is changed directly now with write(). This can
        # be improved further
        for product in products:
            percentage = (
                product.categ_id and product.categ_id.percentage_update or False
            )
            if product.cost_method == "average" and percentage:
                new_standard_price = product.standard_price * (1 + percentage)
                product.write({"standard_price": new_standard_price})

        return moves
