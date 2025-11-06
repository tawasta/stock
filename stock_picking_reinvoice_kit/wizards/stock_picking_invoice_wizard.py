from odoo import fields, models


class StockPickingInvoiceWizard(models.TransientModel):
    _inherit = "stock.picking.invoice.wizard"

    invoice_kit = fields.Boolean(string="Invoice kits", default=False)

    def get_picking_moves(self, picking):
        if self.invoice_kit:
            kit_delivered = 0
            kits = []

            for line in picking.move_line_ids:
                kits.append((line.sale_line_id, 0, 0))
            kits = list(set(kits))

            for kit in kits:
                kit_product = False
                kit = list(kit)
                kit[1] = []
                for line in picking.move_line_ids:
                    if line.sale_line_id and kit[0] == line.sale_line_id:
                        bom = (
                            self.env["mrp.bom"]
                            .sudo()
                            ._bom_find(
                                product=kit[0].product_id,
                            )
                        )
                        if bom:
                            for bom_line in bom.bom_line_ids:
                                if line.product_id == bom_line.product_id:
                                    if line.qty_done <= 0:
                                        check_line = 0
                                    else:
                                        check_line = int(
                                            line.qty_done / bom_line.product_qty
                                        )
                                    kit[1].append(check_line)

                    if kit and kit[0]:
                        bom = (
                            self.env["mrp.bom"]
                            .sudo()
                            ._bom_find(
                                # product=line.sale_line_id.product_id,
                                product=kit[0].product_id,
                            )
                        )
                        if bom.type == "phantom":
                            kit_product = kit[0].product_id
                        else:
                            kit_product = None
                    else:
                        kit_product = None

                if not kit[1]:
                    min_qty = 0
                else:
                    min_qty = min(kit[1])

                for line in picking.move_line_ids:
                    if kit[0] == line.sale_line_id:
                        kit_delivered = min_qty

                if kit_product:
                    yield (kit_product, line.move_id, kit_delivered)
        else:
            for move in picking.move_lines:
                yield (move.product_id, move, move.quantity_done)
