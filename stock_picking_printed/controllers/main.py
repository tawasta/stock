import json
from odoo import http
from odoo import fields
from odoo.http import request
from odoo.addons.web.controllers.main import ReportController


class PickingReportController(ReportController):
    @http.route()
    def report_download(self, data, token):

        res = super(PickingReportController, self).report_download(data, token)
        requestcontent = json.loads(data)
        url, report_type = requestcontent[0], requestcontent[1]

        pattern = "/report/pdf/" if report_type == "qweb-pdf" else "/report/text/"
        reportname = url.split(pattern)[1].split("?")[0]

        if "/" in reportname:
            reportname, docids = reportname.split("/")

            if "." in reportname:
                # Just use the report name ending to allow overriding the print
                module, reportname = reportname.split(".")

            if reportname in ["stock.report_picking", "report_picking"]:
                ids = [int(x) for x in docids.split(",")]

                stock_picking_ids = request.env["stock.picking"].browse(ids)
                stock_picking_ids.write({"picking_printed": fields.Datetime.now()})

        return res
