import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move"

    # Field needs to be stored so that SO lines can be grouped by it
    sh_product_tag_ids = fields.Many2one(
        string="Tags",
        comodel_name="sh.product.tag",
        store=True,
    )

    @api.model
    def create(self, vals):
        product = vals.get("product_id", False)
        if product:
            prod = self.sudo().env["product.product"].search([("id", "=", product)])
            tags = prod.sh_product_tag_ids
            vals["sh_product_tag_ids"] = tags and tags[0].id or False
        return super().create(vals)

    @api.onchange("product_id")
    def onchange_sh_product_tag_ids(self):
        tags = self.product_id.sh_product_tag_ids
        self.sh_product_tag_ids = tags and tags[0].id or False

    def _cron_stock_move_sh_product_tags(self, moves):
        for move in moves:
            tags = move.product_id.sh_product_tag_ids
            move.sh_product_tag_ids = tags and tags[0].id or False
        return moves, "Success"

    def get_stock_moves_to_update_sh_tags(self):
        products = self.env["product.product"].search(
            [("sh_product_tag_ids", "!=", False)]
        )
        moves = self.env["stock.move"].search([("product_id", "in", products.ids)])

        for start in range(0, len(moves), 50):
            yield moves[start : start + 50]

    def cron_compute_sh_product_tag_ids(self):
        """Computes all Stock Move sh_product_tag_ids values"""
        moves = self.get_stock_moves_to_update_sh_tags()

        for batch in moves:
            job_desc = _(f"Assign SH product tags to stock moves: {batch.ids}")
            self.with_delay(description=job_desc)._cron_stock_move_sh_product_tags(
                batch
            )

        _logger.info("Cron Compute SH product tags completed")
