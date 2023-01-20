from odoo import fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    dispatch_note_text = fields.Char(
        string="Note", size=128, help="Text shown on the dispatch note"
    )

    freight_payer = fields.Char(string="Freight paid by")

    contract_number = fields.Char(string="Customer / Contract number")

    customer_contact = fields.Many2one(
        "res.partner", related="sale_id.customer_contact_id"
    )

    container_count = fields.Integer(
        string="Number of containers",
        default=1,
    )

    transport_company = fields.Char(string="Transport Company")

    header_text = fields.Char(string="Dispatch Note Header")
