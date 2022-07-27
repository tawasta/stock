from odoo import fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    effective_date = fields.Date(related="sale_id.effective_date", store=True)
