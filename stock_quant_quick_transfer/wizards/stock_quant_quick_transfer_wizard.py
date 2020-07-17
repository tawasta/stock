from odoo import api, models, fields


class StockQuantQuickTransferWizard(models.TransientModel):

    _name = "stock.quant.quick.transfer.wizard"
    _description = "Quickly transfer a quant"

    quant_id = fields.Many2one(
        comodel_name="stock.quant", string="Quant", required=True,
    )

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        compute="_compute_partner",
        required=True,
    )

    commercial_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Commercial partner",
        compute="_compute_partner",
        required=True,
    )

    location_id = fields.Many2one(
        comodel_name="stock.location", string="Source Location", required=True,
    )

    location_dest_id = fields.Many2one(
        comodel_name="stock.location", string="Destination Location", required=True,
    )

    @api.onchange("location_id")
    def _compute_partner(self):
        for record in self:
            partner = record.location_id.partner_id

            record.partner_id = partner.id
            record.commercial_partner_id = partner.commercial_partner_id.id

    @api.multi
    def create_stock_picking(self):
        quant = self.quant_id

        internal_picking = self.env.ref("stock.picking_type_internal")

        move_lines = [
            (
                0,
                False,
                dict(
                    name=internal_picking.sequence_id.next_by_id(),
                    picking_type_id=internal_picking.id,
                    company_id=quant.company_id.id,
                    product_id=quant.product_id.id,
                    product_uom_qty=quant.qty,
                    product_uom=quant.product_uom_id.id,
                    location_id=self.location_id.id,
                    location_dest_id=self.location_dest_id.id,
                    date_expected=fields.Datetime.now(),
                    scrapped=False,
                    state="draft",
                ),
            )
        ]

        picking = self.env["stock.picking"].create(
            dict(
                location_id=self.location_id.id,
                location_dest_id=self.location_dest_id.id,
                picking_type_id=internal_picking.id,
                move_lines=move_lines,
                state="draft",
            )
        )

        # Confirm
        picking.action_confirm()

        # Reserve
        picking.action_assign()

        # Assign serials. The loop should have only one line
        if quant.lot_id:
            OperationLot = self.env["stock.pack.operation.lot"]
            for packing in picking.pack_operation_product_ids:
                packing.pack_lot_ids = OperationLot.create(
                    dict(
                        operation_id=packing.id,
                        lot_id=quant.lot_id.id,
                        qty_done=quant.qty,
                    )
                )

        packing.qty_done = quant.qty

        picking.do_new_transfer()

        # Refresh the original view
        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }
