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
- Barcode scanning wizard that automatically associates scanned products with stock moves.
- Form and tree views for managing stock receipts and lines.
- Chatter integration for logging receipt confirmation messages.
- Access rights configured for base user groups.

Configuration
=============
No special configuration is needed. The module uses default Odoo access groups and assumes
products and stock moves exist with appropriate barcodes.

Usage
=====
1. Install the module in your Odoo instance.
2. Navigate to the "Stock Receipts" menu under Inventory settings.
3. Use the "Create Stock Receipt" wizard to scan or enter product barcodes.
4. Confirm the receipt to create stock receipt records and log the transaction.

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
