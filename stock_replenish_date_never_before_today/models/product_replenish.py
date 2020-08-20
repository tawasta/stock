from odoo import fields, models


class ProductReplenish(models.TransientModel):
    _inherit = 'product.replenish'
    _description = 'Product Replenish - Date never before today'

    def _prepare_run_values(self):
        res = super(ProductReplenish, self)._prepare_run_values()
        if self.date_planned < fields.Datetime.now():
            res['date_planned'] = fields.Datetime.now()

        return res
