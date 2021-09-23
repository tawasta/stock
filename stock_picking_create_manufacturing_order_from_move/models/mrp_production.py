from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    created_from_stock_move = fields.One2many(
        comodel_name="stock.move", inverse_name="manufacturing_order_id"
    )

    @api.multi
    def button_mark_done(self):
        res = super().button_mark_done()

        for stock in self.created_from_stock_move:
            stock.mo_to_complete = False

        return res

    def find_stock_move_product_with_bom(self, origin, product):
        # This should be changed later on to use some id instead of origin
        stock_move = self.env["stock.move"].search(
            [("origin", "=", origin), ("product_id", "=", product)]
        )
        return stock_move

    @api.model
    def create(self, vals):
        product = vals.get("product_id", False)
        origin = vals.get("origin", False)
        stock_move = self.find_stock_move_product_with_bom(origin, product)
        res = super().create(vals)
        if stock_move:
            # Not a great way to do this, but it avoids singleton error..
            stock_move = stock_move[0]
            stock_move.manufacturing_order_id = res.id
            stock_move.mo_has_been_created = True
            stock_move.mo_to_complete = True
        return res
