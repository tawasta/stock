.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================================
Delivery Slip with Prices as a Separate Print
=================================================

* Adds a second delivery slip print, "Delivery Slip (with prices)", that shows
  the unit prices, discounts, taxes and totals of the related sale order. The
  print is offered on outgoing deliveries only.
* The standard "Delivery Slip" print never shows prices
* Whether prices are shown depends only on the chosen print, not on the
  partner. The partner's "Valued picking" setting is hidden because it has no
  effect.
* Product barcodes are shown on both prints

Configuration
=============

* No configuration needed

Usage
=====

* Open a delivery order and choose Print > Delivery Slip for the slip
  without prices, or Print > Delivery Slip (with prices) for the slip with
  prices

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

This module is maintained by Futural Oy.
