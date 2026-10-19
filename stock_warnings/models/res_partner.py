from odoo import fields, models

from odoo.addons.partner_warnings.models.partner_warning_mixin import WARNING_LEVELS


class ResPartner(models.Model):
    _inherit = "res.partner"

    picking_warn_level = fields.Selection(
        selection=WARNING_LEVELS,
        string="Stock Warning Level",
        default="popup_warning",
    )
