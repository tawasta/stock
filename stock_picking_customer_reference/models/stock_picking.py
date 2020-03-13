from odoo import fields, models


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    customer_reference = fields.Char(
        string="Customer Reference"
    )

    from_purchase_order = fields.Boolean(
        compute="_compute_picking_from_sale_order"
    )

    def _compute_picking_from_sale_order(self):
        for picking in self:
            picking_from = picking.group_id and picking.group_id.name or ''
            picking.from_purchase_order = picking_from.startswith('PO')
