from odoo import api, fields, models
from odoo.tools.float_utils import float_is_zero


class StockQuant(models.Model):

    _inherit = 'stock.quant'

    value = fields.Monetary(
        string='Value', compute='_compute_value', groups='stock.group_stock_manager'
    )

    currency_id = fields.Many2one(
        related='product_id.currency_id', groups='stock.group_stock_manager'
    )

    @api.depends('quantity')
    def _compute_value(self):
        for quant in self:
            if not quant.location_id._should_be_valued() or\
                    (quant.owner_id and quant.owner_id !=
                     quant.company_id.partner_id):
                quant.value = 0
                continue
            if quant.product_id.cost_method == 'fifo':
                quantity = quant.product_id.quantity_svl
                if float_is_zero(
                        quantity,
                        precision_rounding=quant.product_id.uom_id.rounding):
                    quant.value = 0.0
                    continue
                avg_cost = quant.product_id.value_svl / quantity
                quant.value = quant.quantity * avg_cost
            else:
                quant.value = quant.quantity * quant.product_id.standard_price

    @api.model
    def read_group(
            self, domain, fields, groupby, offset=0, limit=None, orderby=False,
            lazy=True):
        if 'value' not in fields:
            return super(StockQuant, self).\
                read_group(domain, fields, groupby, offset=offset,
                           limit=limit, orderby=orderby, lazy=lazy)
        res = super(StockQuant, self).read_group(domain, fields, groupby,
                                                 offset=offset, limit=limit,
                                                 orderby=orderby, lazy=lazy)
        for group in res:
            if group.get('__domain'):
                quants = self.search(group['__domain'])
                group['value'] = sum(quant.value for quant in quants)
        return res
