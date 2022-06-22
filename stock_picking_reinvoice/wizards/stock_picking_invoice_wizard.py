from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockPickingInvoiceWizard(models.TransientModel):

    _name = "stock.picking.invoice.wizard"
    _description = "Create invoice from pickings"

    partner_id = fields.Many2one(
        string="Customer", comodel_name="res.partner", required=True
    )

    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        required=True,
    )

    existing_invoice_id = fields.Many2one(
        string="Existing invoice",
        comodel_name="account.move",
        domain=[("state", "=", "draft")],
        help="Select this to combine new lines to an existing invoice",
    )

    group_lines = fields.Boolean(
        string="Group lines",
        default=True,
        help="If the invoice already has a line for product in this picking, "
        "add quantity to the existing line",
    )

    @api.onchange("partner_id")
    def onchange_partner_id_update_pricelist(self):
        for record in self:
            if record.partner_id:
                record.pricelist_id = record.partner_id.property_product_pricelist

    def action_create_invoice(self):

        picking_ids = self.env["stock.picking"].browse(self._context.get("active_ids"))

        invoice = self.existing_invoice_id
        aml = self.env["account.move.line"]
        existing_line = False

        if not invoice:
            invoice = self.env["account.move"].create(
                {
                    "partner_id": self.partner_id.id,
                    "move_type": "out_invoice",
                }
            )

        for picking in picking_ids:
            if picking.state != "done":
                raise UserError(
                    _(
                        "You can't invoice a picking that is not done: {}".format(
                            picking.name
                        )
                    )
                )

            if picking.invoice_id and picking.invoice_id.state != "cancel":
                raise UserError(
                    _("Picking is already invoiced: {}".format(picking.name))
                )

            partner = picking.partner_id
            # Dummy variable, if we want to re-implement adding move names
            # to invoice line description later
            show_moves = False

            for move in picking.move_lines:
                product = move.product_id
                quantity = move.quantity_done
                account = (
                    product.property_account_income_id
                    or product.categ_id.property_account_income_categ_id
                )
                price = self.pricelist_id.get_product_price(product, quantity, partner)
                if show_moves:
                    line_name = "{} - {}".format(move.name, move.picking_id.name)
                else:
                    line_name = product.display_name

                if self.group_lines:
                    # Try to find existing invoice line
                    existing_line = aml.search(
                        [
                            ("product_id", "=", product.id),
                            ("move_id", "=", invoice.id),
                        ]
                    )

                if existing_line:
                    new_line_values = {
                        "quantity": existing_line.quantity + quantity,
                    }
                    if show_moves:
                        new_line_values["name"] = (
                            "{}, {}".format(existing_line.name, move.picking_id.name),
                        )

                    existing_line.write(new_line_values)
                else:
                    tax = (
                        product.taxes_id and [(6, 0, [product.taxes_id[0].id])] or False
                    )

                    aml.create(
                        {
                            "name": line_name,
                            "price_unit": price,
                            "quantity": quantity,
                            "move_id": invoice.id,
                            "product_id": product.id,
                            "product_uom_id": move.product_uom.id,
                            "tax_ids": tax,
                            "account_id": account.id,
                        }
                    )

            picking.invoice_id = invoice.id
        return invoice, picking_ids
