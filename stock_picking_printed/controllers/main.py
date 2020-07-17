import json
from odoo import http
from odoo import fields
from odoo.http import request
from odoo.addons.web.controllers.main import ReportController


class PickingReportController(ReportController):
    @http.route(["/report/download"], type="http", auth="user")
    def report_download(self, data, token):

        res = super(PickingReportController, self).report_download(data, token)
        requestcontent = json.loads(data)
        url, report_type = requestcontent[0], requestcontent[1]

        pattern = "/report/pdf/" if report_type == "qweb-pdf" else "/report/text/"
        reportname = url.split(pattern)[1].split("?")[0]

        if "/" in reportname:
            reportname, docids = reportname.split("/")
            ids = [int(x) for x in docids.split(",")]

            if reportname == "stock.report_picking":
                stock_picking_ids = request.env["stock.picking"].browse(ids)
                stock_picking_ids.write({"picking_printed": fields.Datetime.now()})

        return res
