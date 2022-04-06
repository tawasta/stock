from odoo import models, fields, api


class StockInventoryLine(models.Model):

    _inherit = "stock.inventory.line"

    price_unit = fields.Float(
        string="Unit Price",
        compute="_compute_standard_price",
        store=True,
        readonly=False,
        help="Technical field used to set the product quant cost",
        # The digits-attribute is not provided,
        # as the stock.move price_unit won't have it either
    )

    @api.onchange("product_id")
    @api.depends("product_id")
    def onchange_product_id_update_cost(self):
        for record in self:
            if record.product_id:
                record.price_unit = record.product_id.standard_price

    @api.depends("product_id")
    def _compute_standard_price(self):
        for record in self:
            if record.product_id:
                record.price_unit = record.product_id.standard_price
            else:
                record.price_unit = 0

    def _get_move_values(self, *args, **kwargs):
        # Add manual cost price to lines

        res = super(StockInventoryLine, self)._get_move_values(*args, **kwargs)

        res["price_unit"] = self.price_unit

        return res
