from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    percentage_update = fields.Float(
        string="Percentage update to price",
        copy=False,
    )

    rule_tip = fields.Char(compute="_compute_rule_tip")

    @api.depends_context("lang")
    @api.depends("percentage_update")
    def _compute_rule_tip(self):
        self.rule_tip = False
        for category in self:
            if category.percentage_update:
                original_total = (30 * 120 + (35 * 10)) / (120 + 10)
                total = original_total * (1 + category.percentage_update)
                category.rule_tip = self.env._(
                    "For example:\n"
                    "Product X current cost is 30€.\n"
                    "Available quantity is 120 Units.\n"
                    "Purchased price is 35€ with 10 Units.\n\n"
                    "Then the new cost for a product is:\n"
                    "(30€ * 120 + (35€ * 10) / (120 + 10))"
                    " * (1 + %(perc)s) = %(tot)s\n\n"
                    "The original cost would had been: %(orig_total)s",
                    perc=category.percentage_update,
                    tot=total,
                    orig_total=original_total,
                )
            else:
                category.rule_tip = False
