from odoo import api, fields, models

from odoo.addons import decimal_precision as dp


class StockPicking(models.Model):

    _inherit = "stock.picking"

    total_compute_volume = fields.Float(
        string="Total Volume",
        digits_compute=dp.get_precision("Stock Weight"),
        compute=lambda self: self._compute_calculate_volume(),
    )

    volume_uom_name = fields.Char(related="move_lines.product_id.volume_uom_name")

    def _compute_calculate_volume(self):
        """Calculate the total volume for the whole
        picking by summing the line volumes"""

        for picking in self:
            total = 0.0
            for line in picking.move_lines:
                total += line.product_id.volume * line.product_uom_qty

            picking.total_compute_volume = total

    @api.model
    def read_group(
        self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True
    ):
        res = super(StockPicking, self).read_group(
            domain,
            fields,
            groupby,
            offset=offset,
            limit=limit,
            orderby=orderby,
            lazy=lazy,
        )
        if "total_compute_volume" in fields:
            for line in res:
                if "__domain" in line:
                    lines = self.search(line["__domain"])
                    total_compute_volume = 0.0
                    for record in lines:
                        total_compute_volume += record.total_compute_volume
                    line["total_compute_volume"] = total_compute_volume

        return res
