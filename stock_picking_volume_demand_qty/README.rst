.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================
Stock Picking Volume Demand Qty
===============================

This module changes the stock move volume calculation to always use the
demand quantity (``product_uom_qty``) instead of the reserved quantity.

The standard ``stock_picking_volume`` module calculates the volume of
stock moves based on the reserved quantity when a move is partially or
fully assigned. This can cause the total volume of a delivery order to
change depending on stock availability.

With this module installed, the volume always represents the full
requested quantity of the delivery order, regardless of reservation
status.

Configuration
=============
No configuration is required.

Usage
=====

After installation, the volume of stock moves and delivery orders is
calculated using the demand quantity of each stock move.

Example:

* Ordered quantity: 10 pcs
* Reserved quantity: 2 pcs
* Product volume: 2 m³

Standard behavior:

* Volume = 2 × 2 m³ = 4 m³

Behavior with this module:

* Volume = 10 × 2 m³ = 20 m³

This allows warehouse and logistics personnel to estimate the total
required shipment volume independently of stock reservations.

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
