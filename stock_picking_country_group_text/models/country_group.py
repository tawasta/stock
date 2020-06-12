from odoo import fields, models


class CountryGroup(models.Model):

    _inherit = "res.country.group"

    stock_picking_text = fields.Text(
        string="Stock Picking Text",
        help="Text to be added on stock pickings going to customers in this "
        + "country group.",
    )

    delivery_slip_text = fields.Text(
        string="Delivery Slip Text",
        help="Text to be added on stock pickings going to customers in this "
        + "country group.",
    )
