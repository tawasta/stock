from odoo import fields, models


class StockMoveCreateManufacturingOrderMessage(models.TransientModel):

    _name = "stock.move.create.manufacturing.order.message"
    _description = "Create MO from stock move - message"

    delivery_message = fields.Text(string="Delivery Message")
    mo_message = fields.Text(string="MO Message")
