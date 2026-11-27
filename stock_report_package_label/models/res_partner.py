from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    package_label_address_id = fields.Many2one(
        "res.partner", string="Package Label address", copy=False
    )
