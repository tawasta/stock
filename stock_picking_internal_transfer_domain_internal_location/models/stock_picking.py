from odoo import api, fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)

        type_id = values.get("picking_type_id", False)

        if type_id and "internal_transfer" in fields_list:
            picking_type = self.env["stock.picking.type"].search([("id", "=", type_id)])
            if picking_type.code == "internal":
                values["internal_transfer"] = True
            else:
                values["internal_transfer"] = False

        return values

    internal_transfer = fields.Boolean(copy=False)
