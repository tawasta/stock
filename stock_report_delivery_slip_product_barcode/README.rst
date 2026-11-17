.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============================================================
Stock Picking: Product Barcodes on Delivery Slip Print's Lines
==============================================================

* Show products' barcodes on Delivery Slip lines, also when lot/serial
  numbers are printed on the delivery slip

Configuration
=============

* Configure the option in Settings > Inventory > Delivery Slip Scannable
  Product Barcodes to choose whether to show the visual barcodes on the
  delivery slip print or just numeric EAN codes.

Usage
=====

* Just print the delivery document's delivery slip print

Known issues / Roadmap
======================

* Consider adding a configurable table heading text instead
  of just 'EAN'

Changelog
=========

* 19.0.1.0.1: Fix missing barcode column on done delivery slips that print
  lot/serial numbers. Remove the unneeded dependency on ``delivery``.
* 19.0.1.0.0: Added option to show product barcodes on delivery slip print's
  lines. During migration from v17 to v19.

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@futural.fi>
* Joonas Lahtinen <joonas.lahtinen@futural.fi>
* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy.
