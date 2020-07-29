from odoo import api, models, fields, _
from odoo.exceptions import UserError


class StockPickingPackWizard(models.TransientModel):

    _name = "stock.picking.packing.wizard"
    _description = "Pack picking quickly"

    package_amount = fields.Integer(string="Packages", default=1)
    delivery_packaging_id = fields.Many2one(
        "product.packaging", default=lambda self: self._default_delivery_packaging_id()
    )
    shipping_weight = fields.Float(string="Shipping weight",)
    package_weight = fields.Float(
        string="Package weight", compute="_compute_package_weight"
    )
    package_logic = fields.Selection(
        string="Packaging logic",
        selection=[("merge", "Don't split lines"), ("split", "Split lines")],
        default="merge",
    )

    def _default_delivery_packaging_id(self):
        res = None
        if self.env.context.get("default_delivery_packaging_id"):
            res = self.env["product.packaging"].browse(
                self.env.context["default_delivery_packaging_id"]
            )
        return res

    @api.onchange("package_amount", "shipping_weight")
    def _compute_package_weight(self):
        for record in self:
            if not record.package_amount or not record.shipping_weight:
                continue
            record.package_weight = record.shipping_weight / record.package_amount

    @api.multi
    def action_create_packages(self):
        picking_ids = self.env["stock.picking"].browse(self._context.get("active_ids"))

        if self.package_logic != "merge":
            raise UserError(_("Selected packaging logic is not supported"))

        for picking in picking_ids:
            lines = picking.move_line_ids_without_package

            if picking.has_packages:
                raise UserError(
                    _(
                        "Picking already has packages. "
                        "Please package rest of the products manually"
                    )
                )

            if self.package_amount > len(lines):
                raise UserError(
                    "{}. {}".format(
                        _("Splitting one line to multiple packages is not supported."),
                        _("Please try with fewer packages"),
                    )
                )

            # Create packages
            stock_package = self.env["stock.quant.package"]
            shipping_weight = self.shipping_weight / self.package_amount
            packages = []
            for i in range(self.package_amount):
                if hasattr(picking, "contents") and picking.contents:
                    contents = picking.contents
                else:
                    contents = picking.origin

                packages.append(
                    stock_package.create(
                        {
                            "packaging_id": self.delivery_packaging_id.id,
                            "shipping_weight": shipping_weight,
                            "contents": contents,
                            "company_id": picking.company_id.id,
                        }
                    )
                )

            for i, line in enumerate(lines):
                # Mark everything as done
                line.move_id.quantity_done = line.move_id.product_uom_qty

                # Mark each line to a package
                line.result_package_id = packages[i % len(packages)]
