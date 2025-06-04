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

        aml = self.env["account.move.line"]
        existing_line = False
        fiscal_position = self.env["account.fiscal.position"]

        # Create new invoice
        invoice_values = {
            "partner_id": self.partner_id.id,
            "move_type": "out_invoice",
            "invoice_date": fields.Datetime.now(),
            "fiscal_position_id": fiscal_position._get_fiscal_position(
                self.partner_id
            ).id,
            "invoice_payment_term_id": self.partner_id.property_payment_term_id.id
            or self.env["account.move"]
            .default_get(["invoice_payment_term_id"])
            .get("invoice_payment_term_id"),
        }

        # Dummy variable, if we want to implement showing picking numbers on origin
        show_pickings = False
        if show_pickings:
            invoice_values["invoice_origin"] = ", ".join(picking_ids.mapped("name"))

        invoice = self.env["account.move"].create(invoice_values)

        for picking in picking_ids:
            if picking.state != "done":
                raise UserError(
                    _(f"You can't invoice a picking that is not done: {picking.name}")
                )

            if picking.invoice_id and picking.invoice_id.state != "cancel":
                raise UserError(_(f"Picking is already invoiced: {picking.name}"))

            # Dummy variable, if we want to re-implement adding move names
            # to invoice line description later
            show_moves = False

            for move in picking.move_ids:
                product = move.product_id
                quantity = move.quantity

                price = self.pricelist_id._get_product_price(
                    product, quantity, currency=invoice.currency_id
                )

                if show_moves:
                    line_name = f"{move.name} - {move.picking_id.name}"
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
                            f"{existing_line.name}, {move.picking_id.name}",
                        )

                    existing_line.with_context(check_move_validity=False).write(
                        new_line_values
                    )
                else:
                    taxes = product.taxes_id.filtered(
                        lambda x: x.company_id == invoice.company_id
                    )
                    tax = taxes and [(6, 0, [taxes[0].id])] or False

                    vals = {
                        "name": line_name,
                        "product_id": product.id,
                        "quantity": quantity,
                        "price_unit": price,
                        "tax_ids": tax,
                    }

                    invoice.write({"invoice_line_ids": [(0, 0, vals)]})

            picking.invoice_id = invoice.id

        # Skip checking move validity, the amount will be computed in the end
        invoice = invoice.with_context(check_move_validity=False)
        invoice._compute_amount()
        invoice._onchange_quick_edit_line_ids()

        # If there is an existing invoice, merge with it
        if self.existing_invoice_id:
            vals = {"date_invoice": invoice.invoice_date}
            invoice_merge = self.env["invoice.merge"].create(vals)
            active_ids = [invoice.id, self.existing_invoice_id.id]
            invoice_merge.with_context(active_ids=active_ids).merge_invoices()

        return invoice, picking_ids
