from odoo import models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    def do_print_picking(self):
        """Prints this module's version of a delivery slip"""
        super().do_print_picking()
        return self.env.ref("stock_report_title.action_report_delivery").report_action(
            self
        )
