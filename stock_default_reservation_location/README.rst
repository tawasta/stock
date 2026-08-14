.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================
Stock Default Reservation Location
==================================

This module extends Odoo stock reservation behavior by prioritizing the
product's configured default stock move location during stock reservation.

When enabled on the operation type, Odoo first attempts to reserve stock
from the location configured in the product's
``default_stock_move_location_id`` field.

If sufficient stock is not available in that location, the reservation
automatically falls back to the standard Odoo reservation logic.

Configuration
=============

#. Go to *Inventory -> Configuration -> Operation Types*.
#. Open the desired operation type.
#. Enable *Use Product Default Location*.

#. Go to *Inventory -> Products*.
#. Open a product.
#. Set *Default Stock Move Location* to the preferred source location.

Usage
=====

When a stock reservation is created:

#. Odoo checks whether *Use Product Default Location* is enabled on the
   operation type.
#. Odoo checks whether the product has a configured
   *Default Stock Move Location*.
#. If stock is available in that location, reservation is performed from
   that location first.
#. If stock is not available, Odoo continues with the standard stock
   reservation flow.

Known issues / Roadmap
======================

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>
* Timo Kekäläinen <timo.kekalainen@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
