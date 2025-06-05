import logging

from odoo import models

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _get_description(self, picking_type_id):
        # Add handling for drop shipping instead of falling back to description field
        self.ensure_one()

        picking_code = picking_type_id.code

        if picking_code == "dropship":
            return self.name
        else:
            return super().get_description(picking_type_id=picking_type_id)
