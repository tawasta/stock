from odoo import models, fields
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP


class StockLocationRoute(models.Model):

    _inherit = 'stock.location.route'

    sale_line_warn = fields.Selection(
        WARNING_MESSAGE,
        string='Sales Order Line',
        help=WARNING_HELP,
        required=True,
        default="no-message"
    )

    sale_line_warn_msg = fields.Text(
        string='Message for Sales Order Line',
    )
