from odoo import _, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_print_custom_labels(self):
        """
        Print a custom label for every product line of the transfer,
        skipping the label type wizard
        """
        self.ensure_one()

        moves = self.move_ids
        if not moves:
            raise UserError(_("Nothing to print: the transfer has no product lines."))

        report = self.env.ref(
            "stock_report_picking_print_custom_label."
            "action_report_stock_move_custom_label"
        )
        return report.report_action(moves)
