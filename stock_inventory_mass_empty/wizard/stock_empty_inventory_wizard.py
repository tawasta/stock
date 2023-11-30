from odoo import api, fields, models


class StockEmptyInventoryWizard(models.TransientModel):

    _name = "stock.empty.inventory.wizard"
    _description = "Stock Empty Inventory Wizard"

    location_names = fields.Text(string="Location names")
    location_ids = fields.Many2many('stock.location', string="Locations", default=lambda self: self.default_locations())

    def default_locations(self):
        return self.env["stock.location"].browse(self._context.get("active_ids"))

    @api.onchange('location_names')
    def onchange_location_name(self):
        locations = self.env["stock.location"]

        if self.location_names:
            split_names = self.location_names.split()
            for name in split_names:
                location = self.env["stock.location"].search([('name', '=', name)], limit=1)
                locations += location
            self.location_ids = locations

    def empty_inventory(self):
        """Empty the selected locations"""
        locations = self.location_ids

        for location in locations:

            quants_with_archived_products = self.env["stock.quant"].search([
                ("location_id", "=", location.id)
                ]).filtered(lambda q: q.product_id.active == False)

            archived_products = quants_with_archived_products.mapped('product_id')

            for product in archived_products:
                product.active = True

            disp_name = location.display_name
            now_date = fields.Datetime.now().date()

            inv_vals = {
                "name": "%s/%s/%s" % ("Adjustment", disp_name, now_date),
                "filter": "none",
                "date": now_date,
                "location_id": location.id,
                "exhausted": False,
            }

            adjustment = self.env["stock.inventory"].create(inv_vals)

            if adjustment:
                adjustment.action_start()
                adjustment.action_reset_product_qty()
                adjustment.action_validate()

            for product in archived_products:
                product.active = False
