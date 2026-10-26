from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.tools import formatLang


class ReportStockMoveCustomLabel(models.AbstractModel):
    _name = "report.stock_report_picking_print_custom_label.sml_label"
    _description = "Stock Move Custom Label"

    def _get_report_values(self, docids, data):
        if not docids:
            raise UserError(_("No stock move lines selected for printing."))

        moves = self.env["stock.move"].browse(docids)

        # Show whole-number quantities as integers (32 instead of 32.00),
        # fractional quantities with the UoM decimal precision
        qty_labels = {}
        for move in moves:
            qty = move.product_uom_qty
            if qty == int(qty):
                qty_labels[move.id] = formatLang(self.env, qty, digits=0)
            else:
                qty_labels[move.id] = formatLang(
                    self.env, qty, dp="Product Unit of Measure"
                )

        return {
            "docs": moves,
            "qty_labels": qty_labels,
            "today": fields.Date.context_today(self),
        }
