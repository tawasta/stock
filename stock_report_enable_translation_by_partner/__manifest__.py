##############################################################################
#
#    Author: Futural Oy
#    Copyright 2020 Futural Oy (https://futural.fi)
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
    "name": "Stock Report - Enable report translation by partner language",
    "summary": """Use the language set for Delivery Address in
                  Picking Operations PDF print""",
    "version": "17.0.1.0.0",
    "category": "Stock",
    "website": "https://github.com/tawasta/stock",
    "author": "Futural",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["stock"],
    "data": [
        "data/ir_cron.xml",
        "report/stock_report_view.xml",
        "report/report_file.xml",
    ],
}
