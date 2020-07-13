from odoo import api, models, fields, _
from odoo.exceptions import UserError


class StockPickingInvoiceWizard(models.TransientModel):

    _name = "stock.picking.invoice.wizard"
    _description = "Create invoice from pickings"

    partner_id = fields.Many2one(
        string="Customer", comodel_name="res.partner", required=True
    )

    existing_invoice_id = fields.Many2one(
        string="Existing invoice",
        comodel_name="account.invoice",
        domain=[("state", "=", "draft")],
        help="Select this to combine new lines to an existing invoice",
    )

    @api.multi
    def action_create_invoice(self):

        picking_ids = self.env["stock.picking"].browse(self._context.get("active_ids"))

        invoice = self.existing_invoice_id

        if not invoice:
            invoice = self.env["account.invoice"].create(
                {"partner_id": self.partner_id.id}
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

            if picking.invoice_id:
                raise UserError(
                    _("Picking is already invoiced: {}".format(picking.name))
                )

            for move in picking.move_lines:
                product = move.product_id
                account = (
                    product.property_account_income_id
                    or product.categ_id.property_account_income_categ_id
                )

                line_name = "{} - {}".format(move.name, move.picking_id.name)

                self.env["account.invoice.line"].create(
                    {
                        "invoice_id": invoice.id,
                        "product_id": product.id,
                        "name": line_name,
                        "quantity": move.quantity_done,
                        "uom_id": move.product_uom.id,
                        "price_unit": abs(move.price_unit),
                        "account_id": account.id,
                    }
                )

            picking.invoice_id = invoice.id
