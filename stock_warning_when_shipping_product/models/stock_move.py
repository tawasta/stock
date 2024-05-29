from odoo import _, api, models


class StockMove(models.Model):

    _inherit = "stock.move"

    @api.onchange("product_id")
    def warn_user(self):
        title = False
        message = False
        result = {}
        warning = {}
        for rec in self:
            product = rec.product_id
            if product.id is not False:
                if product.stock_line_warn != "no-message":
                    title = _("Warning for %s", product.name)
                    message = product.stock_line_warn_msg
                    warning["title"] = title
                    warning["message"] = message
                    result = {"warning": warning}

                    if product.stock_line_warn == "block":
                        self.product_id = False

                    return result
