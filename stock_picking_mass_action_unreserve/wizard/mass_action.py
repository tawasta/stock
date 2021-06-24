##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2021- Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

# 1. Standard library imports:

# 2. Known third party imports:

# 3. Odoo imports (openerp):
from odoo import fields, api
from odoo.models import TransientModel

# 4. Imports from Odoo modules:

# 5. Local imports in the relative form:

# 6. Unknown third party imports:


class StockPickingMassAction(TransientModel):
    # 1. Private attributes
    _inherit = "stock.picking.mass.action"

    # 2. Fields declaration
    unreserve = fields.Boolean(
        string="Unreserve",
        default=lambda self: self._default_check_unreserve(),
        help="Check this box if you want to unreserve all the selected pickings.",
    )

    # 3. Default methods
    @api.model
    def _default_check_unreserve(self):
        return self.env.context.get("unreserve", False)

    # 4. Compute and search fields, in the same order that fields declaration

    # 5. Constraints and onchanges

    # 6. CRUD methods

    # 7. Action methods
    @api.multi
    def mass_action(self):
        res = super(StockPickingMassAction, self).mass_action()
        if self.unreserve:
            pickings_to_unreserve = self.picking_ids.filtered(
                lambda x: (x.picking_type_code != "incoming")
                and x.is_locked
                and (
                    (
                        x.state in ("assigned", "partially_available")
                        and x.move_type != "one"
                    )
                    or (
                        x.state in ("assigned", "partially_available", "confirmed")
                        and x.move_type == "one"
                    )
                )
            ).sorted(key=lambda r: r.scheduled_date)
            pickings_to_unreserve.do_unreserve()
        return res

    # 8. Business methods
