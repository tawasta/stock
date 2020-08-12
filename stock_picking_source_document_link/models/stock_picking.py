from odoo import api, fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    source_document_link_sale_order = fields.Many2one(
        string="Source Document Link",
        comodel_name="sale.order",
        compute="_compute_source_document_link",
    )

    source_document_link_purchase_order = fields.Many2one(
        string="Source Document Link",
        comodel_name="purchase.order",
        compute="_compute_source_document_link",
    )

    source_document_link_stock_picking = fields.Many2one(
        string="Source Document Link",
        comodel_name="stock.picking",
        compute="_compute_source_document_link",
    )

    @api.depends("origin")
    def _compute_source_document_link(self):
        origin = str(self.origin)

        def get_model_by_name_or_false(model, name):
            links = self.env[model].search([('name', '=', name)])
            if len(links) >= 1:
                return links[0]
            else:
                return False

        if origin.startswith("SO"):
            self.source_document_link_sale_order = \
                get_model_by_name_or_false(
                    'sale.order',
                    origin
                )
        elif origin.startswith("PO"):
            self.source_document_link_sale_order = \
                get_model_by_name_or_false(
                    'purchase.order',
                    origin
                )
        elif origin.startswith("Return of WH"):
            self.source_document_link_stock_picking = \
                get_model_by_name_or_false(
                    'stock.picking',
                    origin.replace("Return of ", ""),
                )
