from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    stock_putaway_default_location = fields.Many2one(
        comodel_name="stock.location",
        related="company_id.stock_putaway_default_location",
        readonly=False,
        store=True,
    )
