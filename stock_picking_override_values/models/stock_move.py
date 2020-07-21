from odoo import models


class StockMove(models.Model):

    _inherit = "stock.move"

    def _get_new_picking_values(self):
        res = super(StockMove, self)._get_new_picking_values()
        config_parameter = self.env["ir.config_parameter"]

        for key, value in res.items():
            param_name = "stock.picking.override.{}".format(key)
            override = config_parameter.sudo().get_param(param_name)

            if override:
                res[key] = override

        return res
