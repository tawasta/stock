from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    kit_product = fields.Boolean(
        string="Is a kit product",
        default=lambda self: self._compute_kit_product(),
        store=True,
        copy=False,
        compute="_compute_kit_product",
    )

    @api.depends("bom_ids", "bom_ids.type")
    def _compute_kit_product(self):
        for record in self:
            bom_types = record.bom_ids.mapped("type")
            kit_product = False
            if bom_types and all(x == "phantom" for x in bom_types):
                kit_product = True

            record.kit_product = kit_product
