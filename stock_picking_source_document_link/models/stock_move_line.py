from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    source_document_link_sale_order = fields.Many2one(
        comodel_name="sale.order",
        related="picking_id.source_document_link_sale_order",
    )

    source_document_link_purchase_order = fields.Many2one(
        comodel_name="purchase.order",
        related="picking_id.source_document_link_purchase_order",
    )

    source_document_link_stock_picking = fields.Many2one(
        comodel_name="stock.picking",
        related="picking_id.source_document_link_stock_picking",
    )
