from collections import Counter

from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _get_delivery_slip_line_groups(self, move_lines):
        """Group ``move_lines`` for the delivery slip report by the sale
        order section/note lines that precede them, mirroring how
        sale.report_saleorder_document walks doc.order_line and tracks a
        "current section" as it goes.
        """
        self.ensure_one()

        groups = []
        consumed_sale_line_ids = set()

        orders = move_lines.move_id.sale_line_id.order_id
        for order in orders:
            product_counts = Counter(
                line.product_id.id for line in order.order_line if not line.display_type
            )

            pending_headers = self.env["sale.order.line"]
            in_header_run = False
            current_group = None

            for line in order.order_line.sorted("sequence"):
                if line.display_type:
                    if not in_header_run:
                        # A new run of section/note lines: whatever was
                        # pending before was never used by a product line
                        # actually present in this delivery, so drop it.
                        pending_headers = self.env["sale.order.line"]
                    pending_headers |= line
                    in_header_run = True
                    current_group = None
                    continue

                in_header_run = False

                if product_counts[line.product_id.id] != 1:
                    # Repeated product: never trust sale_line_id enough to
                    # group it, let it fall through to the ungrouped bucket.
                    continue

                line_move_lines = move_lines.filtered(
                    lambda move_line, line=line: move_line.move_id.sale_line_id == line
                )
                if not line_move_lines:
                    # This order line has nothing in this delivery (e.g. a
                    # partial delivery/backorder).
                    continue

                consumed_sale_line_ids.add(line.id)

                if current_group is None:
                    current_group = [pending_headers, self.env["stock.move.line"]]
                    groups.append(current_group)
                    pending_headers = self.env["sale.order.line"]

                current_group[1] |= line_move_lines

        ungrouped_move_lines = move_lines.filtered(
            lambda move_line: not move_line.move_id.sale_line_id
            or move_line.move_id.sale_line_id.id not in consumed_sale_line_ids
        )

        result = [
            (header, group_move_lines._get_aggregated_product_quantities())
            for header, group_move_lines in groups
        ]
        if ungrouped_move_lines:
            result.append(
                (
                    self.env["sale.order.line"],
                    ungrouped_move_lines._get_aggregated_product_quantities(),
                )
            )
        return result
