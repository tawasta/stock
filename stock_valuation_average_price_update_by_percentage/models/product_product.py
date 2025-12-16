from collections import defaultdict

from odoo import models
from odoo.tools import float_is_zero


class StockMove(models.Model):
    _inherit = "stock.move"

    def product_price_update_before_done(self, forced_qty=None):
        """Modification to the original method to multiply with
        percentage_update field"""
        tmpl_dict = defaultdict(lambda: 0.0)
        # Adapt standard price on incomming moves if
        # the product cost_method is 'average'
        std_price_update = {}
        for move in self:
            if not move._is_in():
                continue
            if move.with_company(move.company_id).product_id.cost_method == "standard":
                continue
            product_tot_qty_available = (
                move.product_id.sudo().with_company(move.company_id).quantity_svl
                + tmpl_dict[move.product_id.id]
            )
            rounding = move.product_id.uom_id.rounding

            valued_move_lines = move._get_in_move_lines()
            quantity = 0
            for valued_move_line in valued_move_lines:
                quantity += valued_move_line.product_uom_id._compute_quantity(
                    valued_move_line.quantity, move.product_id.uom_id
                )

            qty = forced_qty or quantity
            if float_is_zero(product_tot_qty_available, precision_rounding=rounding):
                new_std_price = move._get_price_unit()
            elif float_is_zero(
                product_tot_qty_available + move.product_qty,
                precision_rounding=rounding,
            ) or float_is_zero(
                product_tot_qty_available + qty, precision_rounding=rounding
            ):
                new_std_price = move._get_price_unit()
            else:
                # Get the standard price
                percentage = move.product_id.categ_id.percentage_update
                amount_unit = (
                    std_price_update.get((move.company_id.id, move.product_id.id))
                    or move.product_id.with_company(move.company_id).standard_price
                )
                new_std_price = (
                    (amount_unit * product_tot_qty_available)
                    + (move._get_price_unit() * qty)
                ) / (product_tot_qty_available + qty)

                if percentage:
                    new_std_price = new_std_price * (1 + percentage)

            tmpl_dict[move.product_id.id] += quantity
            # Write the standard price, as SUPERUSER_ID because a warehouse manager
            # may not have the right to write on products
            move.product_id.with_company(move.company_id.id).with_context(
                disable_auto_svl=True
            ).sudo().write({"standard_price": new_std_price})
            std_price_update[move.company_id.id, move.product_id.id] = new_std_price
