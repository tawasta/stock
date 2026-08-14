from odoo import models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def operation_quantities_decrease_internal(self):
        """Decrease quantity to be applied by one with each click."""
        if not self.inventory_quantity:
            self.write({"inventory_quantity": self.quantity})
        self.write({"inventory_quantity": self.inventory_quantity - 1})
