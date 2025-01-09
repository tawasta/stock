##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2019 Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see http://www.gnu.org/licenses/agpl.html
#
##############################################################################

{
    "name": "Stock Package Sticker",
    "summary": "Print Package sticker from pickings",
    "version": "17.0.1.0.0",
    "category": "Reporting",
    "website": "https://gitlab.com/tawasta/odoo/stock",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "stock",
        "web_report_sfs",
        "stock_picking_dispatch_fields",
    ],
    "data": [
        "data/paperformat.xml",
        "report/external_layout.xml",
        "report/package_sticker_call.xml",
        "report/package_sticker_main_content.xml",
        "report/package_sticker_report.xml",
    ],
}
