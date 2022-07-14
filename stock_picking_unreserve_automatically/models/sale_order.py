from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def _default_force_unreserve(self):
        return self.company_id.force_unreserve

    force_unreserve = fields.Boolean(
        copy=False, default=lambda self: self._default_force_unreserve()
    )

    @api.model
    def create(self, vals):
        """Set Force Unreserve value from an order's company"""

        company_id = vals.get("company_id", False)
        if company_id:
            company = self.env["res.company"].search([("id", "=", company_id)])
            vals["force_unreserve"] = company.force_unreserve

        return super().create(vals)
