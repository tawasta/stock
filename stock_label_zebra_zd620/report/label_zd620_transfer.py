from odoo import models


class ReportLabelZd620Transfer(models.AbstractModel):
    _name = "report.stock_label_zebra_zd620.label_zd620_transfer_view"
    _description = "ZD620 Transfer Label Data"

    def _get_report_values(self, docids, data):
        move_lines = self.env["stock.move.line"].browse(data.get("move_line_ids", []))
        lines = [self._get_line_values(move_line) for move_line in move_lines]
        return {
            "lines": lines,
            "company": self.env.company,
        }

    def _get_line_values(self, move_line):
        move = move_line.move_id
        product = move_line.product_id
        picking = move_line.picking_id
        is_outgoing = picking.picking_type_id.code == "outgoing"
        source_document = move._get_source_document()
        lot_name = move_line.lot_id.name or move_line.lot_name
        return {
            "move_line": move_line,
            "product": product,
            "is_outgoing": is_outgoing,
            "default_code": product.default_code or "",
            "barcode": product.barcode or "",
            "quantity": move_line.quantity,
            "uom_name": move_line.product_uom_id.name,
            "lot_name": lot_name if product.tracking != "none" else "",
            "source_document_name": source_document.name if source_document else "",
            "customer_name": picking.partner_id.name or "",
            "customer_reference": (
                getattr(source_document, "client_order_ref", "")
                or getattr(source_document, "partner_ref", "")
                or ""
            ),
            "location_name": move_line.location_id.name if is_outgoing else "",
        }
