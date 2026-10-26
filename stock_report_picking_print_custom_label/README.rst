.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================
Stock Move - Custom Label
=================================

* Adds a "Custom Labels" button to the transfer (stock.picking) form header,
  next to the Print buttons.
* One click prints a label for every product line of the transfer - no print
  menu selection or label wizard configuration needed.
* Each product line is printed on its own A4 landscape page.
* The label shows the product code, product name, demanded quantity, current
  date, source/destination/default locations and the product's EAN code as
  both a barcode image and numeric text.
* The button is hidden on outgoing shipments (deliveries).

Configuration
=============
* Depends on ``stock_move_product_default_location`` for the default location
  field and ``stock_report_label_product_ean_code`` for the EAN code field.

Usage
=====
* Open a transfer, e.g. an internal transfer or a receipt.
* Click the *Custom Labels* button in the form header, next to Print.
* A PDF is downloaded/printed directly, with one label page per product
  line of the transfer.

Known issues / Roadmap
======================
* The barcode symbology is Code128 (matching the existing EAN code module).
  If strict EAN13 formatting is required, the symbology can be changed.

Credits
=======

Contributors
------------

* Joonas Lahtinen <joonas.lahtinen@futural.fi>


Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
