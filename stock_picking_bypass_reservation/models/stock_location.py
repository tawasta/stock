from odoo import fields, models


class StockLocation(models.Model):

    _inherit = "stock.location"

    allow_bypass_reservation = fields.Boolean(
        string="Always allow stock moves",
        help="""When selected, always allow stock moves on this location for every
        product. Negative stock quants are permitted because of this.""",
    )

    def should_bypass_reservation(self):
        res = super(StockLocation, self).should_bypass_reservation()
        if self.allow_bypass_reservation:
            return True
        else:
            return res
