from collections import defaultdict

from odoo import fields, models


class LotLabelLayout(models.TransientModel):
    _inherit = "lot.label.layout"

    print_format = fields.Selection(
        selection_add=[("zd620_lot", "ZD620 Lot Label (76x50mm)")],
        ondelete={"zd620_lot": "set default"},
    )

    def process(self):
        if self.print_format != "zd620_lot":
            return super().process()

        self.ensure_one()
        if self.label_quantity == "lots":
            docids = self.move_line_ids.lot_id.ids
        else:
            uom_unit = self.env.ref("uom.product_uom_unit")
            quantity_by_lot = defaultdict(int)
            for move_line in self.move_line_ids:
                if not move_line.lot_id:
                    continue
                if move_line.product_uom_id._has_common_reference(uom_unit):
                    quantity_by_lot[move_line.lot_id.id] += int(move_line.quantity)
                else:
                    quantity_by_lot[move_line.lot_id.id] += 1
            docids = []
            for lot_id, qty in quantity_by_lot.items():
                docids.extend([lot_id] * qty)

        report_action = self.env.ref(
            "stock_label_zebra_zd620.label_zd620_lot"
        ).report_action(docids, config=False)
        report_action.update({"close_on_report_download": True})
        return report_action
