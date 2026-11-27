from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    sscc = fields.Char(string="SSCC", copy=False, store=True)

    def calculate_sscc_check_digit(self, gtin_identifier):
        total = 0
        multiply = 3

        for num in reversed(gtin_identifier):
            total += int(num) * multiply
            if multiply == 3:
                multiply = 1
            elif multiply == 1:
                multiply = 3

        check_digit = (10 - (total % 10)) % 10
        return check_digit

    def prepare_sscc_code(self):
        self.ensure_one()
        sscc = ""

        sscc_value = self.env["ir.sequence"].next_by_code("stock.picking.sscc")
        extra_digit = False
        company_prefix = False

        company_id = self.company_id or False

        if company_id:
            extra_digit = company_id.sscc_extension_digit
            company_prefix = company_id.sscc_company_prefix

        if extra_digit and company_prefix:
            combined_sscc = f"{extra_digit}{company_prefix}{sscc_value}"
            check_digit = self.calculate_sscc_check_digit(combined_sscc)
            sscc = f"{combined_sscc}{check_digit}"
        return sscc
