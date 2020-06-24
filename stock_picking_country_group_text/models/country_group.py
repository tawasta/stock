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
        help="Text to be added on delivery slip going to customers in this "
        + "country group.",
    )

    dispatch_note_text = fields.Text(
        string="Dispatch Note Text",
        help="Text to be added on dispatch note going to customers in this "
        + "country group.",
    )
