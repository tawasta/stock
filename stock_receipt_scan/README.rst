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

Configuration
=============
No special configuration is needed. The module uses default Odoo access groups and assumes
products and stock moves exist with appropriate barcodes.

Usage
=====
1. Install the module in your Odoo instance.
2. Navigate to the **"Stock Receipts"** menu under Inventory settings to use the traditional stock receipt scan wizard.
3. Alternatively, go to an existing **Stock Picking (Delivery or Receipt)** and use the **"Scan Barcode"** button in the header to:
   - Scan product barcodes using GS1 format.
   - Automatically create stock move lines with lot and expiration data.
   - Review and save scanned data into the picking.
4. Confirm the stock operation or receipt as usual.

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
