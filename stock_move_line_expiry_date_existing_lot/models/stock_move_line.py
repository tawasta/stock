from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    expiration_date_lot = fields.Datetime(
        string="Expiration Date",
        compute="_compute_expiration_date",
        store=True,
        help="This is the date on which the goods with this Serial Number may"
        " become dangerous and must not be consumed.",
    )

    @api.onchange("expiration_date_lot")
    def onchange_expiration_date_lot(self):
        self.expiration_date = self.expiration_date_lot
        self.lot_id.expiration_date = self.expiration_date_lot
