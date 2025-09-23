.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================================
Product scanner for picking creation
====================================

The Stock Receipt Scan module provides an interface and logic for managing stock receipts in Odoo.
The core of the module consists of models for stock receipts and their lines, along with a barcode
scanning wizard for quick receipt creation.

This module contains a wizard to scan barcodes and QR-codes. The wizard creates
receipts, internal transfers and deliveries based on scanned values.

GS1 barcode is parsed by product code (01), lot number (10), and expiration date (17).
The scanned expiration date needs to be in YYMMDD format, meaning the year is first
and then the month and the day. Else the expiration date scanning does not work.

The wizard validates product and lot existence, prevents duplicate scanning of the same
lot/product combination in the session, and allows updating the stock quantities directly
on existing quants. The interface provides a barcode input, a dynamic list of scanned items,
and buttons to apply changes or cancel.

The module also contains:
- Form and tree views for managing stock receipts, lines, and scanned products.
- Chatter integration for logging receipt confirmation messages.

An information pop-up is shown if older stock is found for the same product when
scanning a barcode for an internal transfer or a delivery.

Configuration
=============
"Lots & Serial Numbers" and "Expiration Dates" needs to be enabled
from Inventory settings to use this module.

The module uses default Odoo access groups and assumes products and
stock moves exist with appropriate barcodes.

Usage
=====
1. Install the module in your Odoo instance
2. Go to Inventory Overview and click on "Scan barcodes" in Receipts, Delivery Orders
   or Internal Transfers
3. Alternatively, go to an existing **Stock Picking (Delivery or Receipt)** and use
   the **"Scan Barcode"** button in the header to:
   - Scan product barcodes using GS1 format.
   - Automatically create stock move lines with lot and expiration data.
   - Review and save scanned data into the picking.
4. Use the **Barcode Transfer Wizard** to scan barcodes and quickly create internal
   stock transfers, receipts or deliveiries by scanning GS1 barcodes that include
   product, lot, and expiration date information.
   - Validate the scanned data against existing stock quants.
   - Edit quantities of scanned lots inline.

Known issues / Roadmap
======================
A new lot is created for incoming shipments if the lot does not exist already.
So it is possible to created several empty lots by using this functionality.

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>
* Timo Kekäläinen <timo.kekalainen@tawasta.fi>
* Jarmo Kortetjärvi <jarmo.kortetjarvi@tawasta.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
