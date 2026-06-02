from odoo import models
from odoo.tools.float_utils import float_compare


class StockMove(models.Model):
    _inherit = "stock.move"

    def _update_reserved_quantity(
        self,
        need,
        location_id,
        quant_ids=None,
        lot_id=None,
        package_id=None,
        owner_id=None,
        strict=True,
    ):
        """
        Extend Odoo stock reservation behavior.

        When the picking type has use_default_location enabled and the
        product has default_stock_move_location_id configured, reservation
        is first attempted from that location.

        If stock is not available there, the standard Odoo reservation
        flow is used through super().

        This customization only influences reservation source selection
        and does not replace the standard Odoo reservation mechanism.
        """
        self.ensure_one()

        default_location = self.product_id.product_tmpl_id.default_stock_move_location_id

        if not (
            self.picking_type_id.use_default_location
            and default_location
            and default_location.usage == "internal"
        ):
            return super()._update_reserved_quantity(
                need,
                location_id,
                quant_ids=quant_ids,
                lot_id=lot_id,
                package_id=package_id,
                owner_id=owner_id,
                strict=strict,
            )

        available_qty = self.env["stock.quant"]._get_available_quantity(
            self.product_id,
            default_location,
            lot_id=lot_id,
            package_id=package_id,
            owner_id=owner_id,
            strict=True,
        )

        if float_compare(
            available_qty,
            0.0,
            precision_rounding=self.product_id.uom_id.rounding,
        ) <= 0:
            return super()._update_reserved_quantity(
                need,
                location_id,
                quant_ids=quant_ids,
                lot_id=lot_id,
                package_id=package_id,
                owner_id=owner_id,
                strict=strict,
            )

        reserved_qty = super()._update_reserved_quantity(
            min(need, available_qty),
            default_location,
            quant_ids=quant_ids,
            lot_id=lot_id,
            package_id=package_id,
            owner_id=owner_id,
            strict=True,
        )

        remaining_qty = need - reserved_qty

        if float_compare(
            remaining_qty,
            0.0,
            precision_rounding=self.product_id.uom_id.rounding,
        ) > 0:
            reserved_qty += super()._update_reserved_quantity(
                remaining_qty,
                location_id,
                quant_ids=quant_ids,
                lot_id=lot_id,
                package_id=package_id,
                owner_id=owner_id,
                strict=strict,
            )

        return reserved_qty