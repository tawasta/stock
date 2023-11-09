from odoo import fields, models


class StockEmptyInventoryWizard(models.TransientModel):

    _name = "stock.empty.inventory.wizard"
    _description = "Stock Empty Inventory Wizard"

    location_names = fields.Text(string="Location names")
    location_ids = fields.Many2one('stock.location', string="Locations")

    @api.onchange('location_name')
    def onchange_location_name(self):
        split_names = self.location_names.split()
        for name in split_names:
            self.location_ids |= self.env["stock.location"].search([('name', '=', name), limit=1])

    def empty_inventory(self):
        """Empty the selected locations"""
        if not self.location_ids:
            locations = self.env["stock.location"].browse(self._context.get("active_ids"))
            self.location_ids = locations
        else:
            locations = self.location_ids

        for location in locations:
            quants = self.env['stock.quant'].search([('location_id', 'child_of', location.id)])

            if not quants:
                continue

            products = [q.product_id for q in quants]

            disp_name = location.display_name
            now_date = fields.Datetime.now().date()

            inv_vals = {
                "name": "{}/{}/{}".format("Adjustment", disp_name, now_date),
                "filter": "partial",
                "date": now_date,
                "location_id": [(6, 0, [location.id])],
                "product_ids": [(6, 0, products)],
                "exhausted": True,
            }

            adjustment = self.env["stock.inventory"].create(inv_vals)

            if adjustment:
                adjustment.action_start()
                adjustment.line_ids.action_reset_product_qty()
                adjustment.action_validate()
