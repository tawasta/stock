
from odoo import models


class ReturnPicking(models.TransientModel):

    _inherit = 'stock.return.picking'

    def sudo_create_returns(self):
        return self.sudo().create_returns()
