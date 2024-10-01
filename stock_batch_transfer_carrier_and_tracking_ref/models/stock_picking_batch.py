from odoo import fields, models


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    carrier_id = fields.Many2one("delivery.carrier", string="Carrier", copy=False)
    carrier_tracking_ref = fields.Char(string="Tracking Reference", copy=False)
    batch_ref = fields.Char(
        string="Reference", copy=False, help="Reference for batches."
    )
