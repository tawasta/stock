from odoo import _, api, fields, models
from odoo.tools import float_is_zero


class InventoryLine(models.Model):
    _name = "stock.inventory.line"
    _description = "Inventory Line"
    _order = "product_id, inventory_id, location_id, prod_lot_id"

    is_editable = fields.Boolean(readonly=True)
    inventory_id = fields.Many2one(
        "stock.inventory", "Inventory", index=True, readonly=True
    )
    partner_id = fields.Many2one("res.partner", "Owner", readonly=True)
    product_id = fields.Many2one(
        "product.product", "Product", index=True, readonly=True
    )
    product_uom_id = fields.Many2one(
        "uom.uom", "Product Unit of Measure", readonly=True
    )
    product_qty = fields.Float(
        "Counted Quantity", digits="Product Unit of Measure", readonly=True
    )
    categ_id = fields.Many2one(related="product_id.categ_id", store=True, readonly=True)
    location_id = fields.Many2one(
        "stock.location", "Location", index=True, readonly=True
    )
    package_id = fields.Many2one(
        "stock.quant.package",
        "Pack",
        index=True,
        domain="[('location_id', '=', location_id)]",
        readonly=True,
    )
    prod_lot_id = fields.Many2one(
        "stock.production.lot",
        "Lot/Serial Number",
        domain="[('product_id','=',product_id), ('company_id', '=', company_id)]",
        readonly=True,
    )
    company_id = fields.Many2one(
        "res.company",
        "Company",
        related="inventory_id.company_id",
        index=True,
        store=True,
        readonly=True,
    )
    state = fields.Selection(
        string="Status", related="inventory_id.state", readonly=True
    )
    theoretical_qty = fields.Float(
        "Theoretical Quantity", digits="Product Unit of Measure", readonly=True
    )
    difference_qty = fields.Float(
        "Difference",
        compute="_compute_difference",
        help="""Indicates the gap between the product's theoretical
                quantity and its newest quantity.""",
        digits="Product Unit of Measure",
        search="_search_difference_qty",
        readonly=True,
    )
    inventory_date = fields.Datetime(
        help="Last date at which the On Hand Quantity has been computed.",
        readonly=True,
    )
    product_tracking = fields.Selection(
        string="Tracking", related="product_id.tracking", readonly=True
    )

    @api.depends("product_qty", "theoretical_qty")
    def _compute_difference(self):
        for line in self:
            line.difference_qty = line.product_qty - line.theoretical_qty

    def _search_difference_qty(self, operator, value):
        if operator == "=":
            result = True
        elif operator == "!=":
            result = False
        else:
            raise NotImplementedError()
        if not self.env.context.get("default_inventory_id"):
            raise NotImplementedError(
                _(
                    "Unsupported search on %s outside of an Inventory Adjustment",
                    "difference_qty",
                )
            )
        lines = self.search(
            [("inventory_id", "=", self.env.context.get("default_inventory_id"))]
        )
        line_ids = lines.filtered(
            lambda line: float_is_zero(
                line.difference_qty, precision_rounding=line.product_id.uom_id.rounding
            )
            == result
        ).ids
        return [("id", "in", line_ids)]
