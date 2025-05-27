from odoo import api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        res = super().button_validate()
        pickings = self.filtered(lambda x: not x.purchase_id)

        if not pickings:
            return res

        act = True
        report_actions = self._get_autoprint_report_actions()

        if report_actions:
            for report in report_actions:
                report_ref = report.get("report_name", False)
                report = (
                    report_ref
                    and self.env["ir.actions.report"].search(
                        [("report_name", "=", report_ref)]
                    )
                    or False
                )
                if report:
                    act = report.report_action(pickings)

        return act
