from odoo import _, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    def open_return_picking_view(self):
        view = self.env.ref("stock.view_stock_return_picking_form")
        return {
            "name": _("Reverse Transfer"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "stock.return.picking",
            "views": [(view.id, "form")],
            "view_id": view.id,
            "target": "new",
        }

    def sudo_open_return_picking_view(self):
        return self.sudo().open_return_picking_view()
