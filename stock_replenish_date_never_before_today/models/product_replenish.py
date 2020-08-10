from odoo import fields, models


class ProductReplenish(models.TransientModel):
    _inherit = 'product.replenish'
    _description = 'Product Replenish - Date never before today'

    def _prepare_run_values(self):
        if self.date_planned < fields.Datetime.now():
            self.date_planned_checked = fields.Datetime.now()

        return super(ProductReplenish, self)._prepare_run_values()
