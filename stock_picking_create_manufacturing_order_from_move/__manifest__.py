##############################################################################
#
#    Author: Oy Tawasta OS Technologies Ltd.
#    Copyright 2021 Oy Tawasta OS Technologies Ltd. (https://tawasta.fi)
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
    "name": "Create Manufacturing order from stock picking line",
    "summary": "Create Manufacturing order from stock picking line",
    "version": "12.0.1.0.1",
    "category": "Stock",
    "website": "https://tawasta.fi",
    "author": "Tawasta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["mrp", "stock", "mrp_production_autoprocess_work_orders"],
    "data": [
        "views/mrp_production.xml",
        "views/stock_move.xml",
        "views/stock_picking.xml",
    ],
}
