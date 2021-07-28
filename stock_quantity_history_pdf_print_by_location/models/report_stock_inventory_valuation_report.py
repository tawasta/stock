
from odoo import api, fields, models


class ReportStockInventoryValuationReport(models.TransientModel):

    _inherit = 'report.stock.inventory.valuation.report'

    location_id = fields.Many2one(
        'stock.location', domain=[('usage', 'in', ['internal', 'transit'])],
    )

    @api.multi
    def _compute_results(self):
        self.ensure_one()
        if not self.compute_at_date:
            self.date = fields.Datetime.now()

        products = self.env['product.product'].\
            with_context(dict(to_date=self.date, company_owned=True,
                              create=False, edit=False)).\
            search([
                ('type', '=', 'product'),
                ('qty_available', '!=', 0)
            ])

        quant_products = self.location_id and self.env['stock.quant'].search(
                [('location_id', '=', self.location_id.id)]).mapped(
                        'product_id') or self.env['product.product']

        products = quant_products and products & quant_products or products

        ReportLine = self.env['stock.inventory.valuation.view']
        for product in products:
            standard_price = product.standard_price
            if self.date:
                standard_price = product.get_history_price(
                    self.env.user.company_id.id,
                    date=self.date)

            quant_domain = [
                ('product_id', '=', product.id)
            ]

            if self.location_id:
                quant_domain.append(('location_id', '=', self.location_id.id))

            quants = self.env['stock.quant'].search(
                quant_domain
            )

            quant_value = sum([q.value for q in quants])

            line = {
                'name': product.name,
                'reference': product.default_code,
                'barcode': product.barcode,
                'qty_at_date': product.qty_at_date,
                'uom_id': product.uom_id,
                'currency_id': product.currency_id,
                'cost_currency_id': product.cost_currency_id,
                'standard_price': standard_price,
#                 'stock_value': product.qty_at_date * standard_price,
                'stock_value': quant_value,
                'cost_method': product.cost_method,
            }
            if product.qty_at_date != 0:
                self.results += ReportLine.new(line)
