from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _compute_product_from_vendor_code(self):
        """Assigns Vendor Product Code based on the vendor of a picking."""
        for move in self:
            vendors = move.product_id.seller_ids.filtered(
                lambda s: s.partner_id == move.picking_id.partner_id
            )

            vendor_info = vendors and vendors[0] or False

            move.product_from_vendor_name = (
                vendor_info and vendor_info.product_name or False
            )
            move.product_from_vendor_code = (
                vendor_info and vendor_info.product_code or False
            )

    product_from_vendor_name = fields.Char(
        string="Vendor Product Name", compute="_compute_product_from_vendor_code"
    )
    product_from_vendor_code = fields.Char(
        string="Vendor Product Code", compute="_compute_product_from_vendor_code"
    )
