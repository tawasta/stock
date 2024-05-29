from odoo import api, fields, models

from odoo.addons.base.models.res_partner import WARNING_HELP, WARNING_MESSAGE


class ProductProduct(models.Model):
    _inherit = "product.product"

    stock_line_warn = fields.Selection(
        WARNING_MESSAGE,
        "Stock Picking Line",
        help=WARNING_HELP,
        required=True,
        default="no-message",
        compute="_compute_stock_fields",
        inverse="_inverse_stock_fields",
        store=True,
    )

    stock_line_warn_msg = fields.Text(
        "Message for stock picking",
        compute="_compute_stock_fields",
        inverse="_inverse_stock_fields",
        store=True,
    )

    @api.depends(
        "product_tmpl_id.stock_line_warn", "product_tmpl_id.stock_line_warn_msg"
    )
    def _compute_stock_fields(self):
        for product in self:
            product.stock_line_warn = product.product_tmpl_id.stock_line_warn
            product.stock_line_warn_msg = product.product_tmpl_id.stock_line_warn_msg

    def _inverse_stock_fields(self):
        for product in self:
            product.product_tmpl_id.stock_line_warn = product.stock_line_warn
            product.product_tmpl_id.stock_line_warn_msg = product.stock_line_warn_msg
