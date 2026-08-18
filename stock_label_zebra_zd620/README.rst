.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================
Stock Label: Zebra ZD620
=========================

* Adds three 76mm x 50mm PDF label formats to the standard "Print Labels"
  wizards (``product.label.layout`` and ``lot.label.layout``), for a Zebra
  ZD620 label printer, the same way core's own "Dymo"/"2x7 with price"
  etc. formats work: a dedicated ``report.paperformat`` (76x50mm)

Configuration
=============
\-

Usage
=====
* From a product (list, kanban or form): Action > Print Labels, choose
  "ZD620 Product Label (76x50mm)".
* From an outgoing or incoming transfer: Print > Labels, choose "ZD620
  Transfer Label (76x50mm)".
* From a transfer with tracked lots/serials: Print > Labels > Lot/SN
  Labels, choose "ZD620 Lot Label (76x50mm)".
* From a Lot/Serial Number record directly: gear menu > Print >
  "Lot/Serial Number (ZD620)", next to core's own "(PDF)"/"(ZPL)"
  options.

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
