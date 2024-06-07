from odoo import api, fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    delay_details = fields.Many2one(
        string="Delay detail",
        comodel_name="stock.picking.delay.detail",
        domain=[],
    )

    @api.onchange("delay_reason")
    def _onchange_delay_reason(self):
        for rec in self:
            if rec.delay_details:
                rec.delay_details = False
            if rec.delay_reason:
                return {
                    "domain": {
                        "delay_details": [("delay_reason", "=", self.delay_reason.id)]
                    }
                }
            else:
                return {"domain": {"delay_details": []}}
