.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================
Stock Receipt Scan
==================

The Stock Receipt Scan module provides an interface and logic for managing stock receipts in Odoo.
The core of the module consists of models for stock receipts and their lines, along with a barcode
scanning wizard for quick receipt creation.

Features
========

- Stock Receipt and Stock Receipt Line models with user tracking and timestamps.
- Two separate barcode scanning features:

  1. **Stock Receipt Wizard**: For creating new stock receipt records by scanning product barcodes.
  2. **Picking Barcode Wizard**: Integrated into stock transfers, enabling barcode-based stock move line creation directly from a delivery/receipt.

- GS1 barcode parsing including product code (01), lot number (10), and expiration date (17).
- Form and tree views for managing stock receipts, lines, and scanned products.
- Chatter integration for logging receipt confirmation messages.
- Access rights configured for base user groups.

- **Inventory Update by Barcode Wizard**:

  This new feature provides a transient wizard (`quant.barcode.update.wizard`) allowing users to scan GS1 barcodes and update existing stock inventory quantities quickly. It supports GS1 barcode parsing for:
    - Product code (01)
    - Lot number (10)
    - Expiration date (17)

  The wizard validates product and lot existence, prevents duplicate scanning of the same lot/product combination in the session, and allows updating the stock quantities directly on existing quants. The interface provides a barcode input, a dynamic list of scanned items, and buttons to apply changes or cancel.


- **Internal Transfer Barcode Wizard**:

  This feature provides a transient wizard model (`stock.barcode.transfer.wizard`) that allows scanning GS1 barcodes to create internal stock transfers. It parses GS1 barcodes to extract product codes, lot numbers, and expiration dates, validates stock availability in the selected source location, and creates stock moves for scanned products. The wizard interface includes a barcode input with real-time parsing and a tree view of scanned products and their details. It also restricts the location selection based on scanned lines and offers buttons to create the transfer or cancel.

An information pop-up is shown if older stock is found for the same product when scanning a barcode for
an internal transfer or a delivery.

Configuration
=============
"Lots & Serial Numbers" and "Expiration Dates" needs to be enabled from Inventory settings to use this module.
The module uses default Odoo access groups and assumes products and stock moves exist with appropriate barcodes.

Usage
=====
1. Install the module in your Odoo instance.
2. Navigate to the **"Stock Receipts"** menu under Inventory settings to use the traditional stock receipt scan wizard.
3. Alternatively, go to an existing **Stock Picking (Delivery or Receipt)** and use the **"Scan Barcode"** button in the header to:
   - Scan product barcodes using GS1 format.
   - Automatically create stock move lines with lot and expiration data.
   - Review and save scanned data into the picking.
4. Use the **Internal Transfer Barcode Wizard** to scan barcodes and quickly create internal stock transfers by scanning GS1 barcodes that include product, lot, and expiration date information.
5. Use the **Inventory Update by Barcode Wizard** from the Inventory Update menu to:
   - Scan GS1 barcodes that include product, lot, and expiration data.
   - Validate the scanned data against existing stock quants.
   - Edit quantities of scanned lots inline.
   - Apply inventory quantity updates directly to the stock quants.
6. Confirm the stock operation or receipt as usual.

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>
* Timo Kekäläinen <timo.kekalainen@tawasta.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
