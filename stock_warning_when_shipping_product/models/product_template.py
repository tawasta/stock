from odoo import api, fields, models

from odoo.addons.base.models.res_partner import WARNING_HELP, WARNING_MESSAGE


class ProductTemplate(models.Model):
    _inherit = "product.template"

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
        "product_variant_id.stock_line_warn", "product_variant_id.stock_line_warn_msg"
    )
    def _compute_stock_fields(self):
        for template in self:
            if template.product_variant_id:
                product = template.product_variant_id
                template.stock_line_warn = product.stock_line_warn
                template.stock_line_warn_msg = product.stock_line_warn_msg

    def _inverse_stock_fields(self):
        for template in self:
            if template.product_variant_id:
                product = template.product_variant_id
                product.stock_line_warn = template.stock_line_warn
                product.stock_line_warn_msg = template.stock_line_warn_msg
