from odoo import fields, models


class ProductProduct(models.Model):

    _inherit = 'product.product'

    value_svl = fields.Float(compute='_compute_value_svl')
    quantity_svl = fields.Float(compute='_compute_value_svl')
    stock_valuation_layer_ids = fields.One2many('stock.valuation.layer',
                                                'product_id')

    def _compute_value_svl(self):
        """Compute `value_svl` and `quantity_svl`."""
        company_id = self.env.context.get(
            'force_company', self.env.user.company_id.id)
        domain = [
            ('product_id', 'in', self.ids),
            ('company_id', '=', company_id),
        ]
        if self.env.context.get('to_date'):
            to_date = fields.Datetime.to_datetime(self.env.context['to_date'])
            domain.append(('create_date', '<=', to_date))
        groups = self.env['stock.valuation.layer'].\
            read_group(domain, ['value:sum', 'quantity:sum'], ['product_id'])
        products = self.browse()
        for group in groups:
            product = self.browse(group['product_id'][0])
            product.value_svl = self.env.user.company_id.\
                currency_id.round(group['value'])
            product.quantity_svl = group['quantity']
            products |= product
        remaining = (self - products)
        remaining.value_svl = 0
        remaining.quantity_svl = 0
