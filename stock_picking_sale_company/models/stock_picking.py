from odoo import fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    sale_company_id = fields.Many2one(
        comodel_name="res.company", related="sale_id.company_id", string="Sale Company",
    )
