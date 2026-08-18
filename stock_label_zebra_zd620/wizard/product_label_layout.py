from odoo import fields, models
from odoo.exceptions import UserError


class ProductLabelLayout(models.TransientModel):
    _inherit = "product.label.layout"

    print_format = fields.Selection(
        selection_add=[
            ("zd620_product", "ZD620 Product Label (76x50mm)"),
            ("zd620_transfer", "ZD620 Transfer Label (76x50mm)"),
        ],
        ondelete={
            "zd620_product": "set default",
            "zd620_transfer": "set default",
        },
    )

    def _prepare_report_data(self):
        xml_id, data = super()._prepare_report_data()
        if self.print_format == "zd620_product":
            xml_id = "stock_label_zebra_zd620.label_zd620_product"
        elif self.print_format == "zd620_transfer":
            if not self.move_ids:
                raise UserError(
                    self.env._("Select a transfer to print this label from.")
                )
            xml_id = "stock_label_zebra_zd620.label_zd620_transfer"
            data["move_line_ids"] = self.move_ids.move_line_ids.ids
        return xml_id, data
