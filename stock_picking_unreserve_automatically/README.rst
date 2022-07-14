.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================================
Stock Picking - Unreserve automatically
=======================================

Set sale orders to automatically unreserve deliveries. The functionality is
company dependent, so different companies may choose to have reservation
enabled. Odoo can do the same automatic unreservation, but it cannot be set
to work with the same kind of company dependency that this module serves.

Configuration
=============

VERY IMPORTANT PART!!! PLEASE READ IT BEFORE USE!!!
This module does not work with procurement_jit module, because it will reserve
delivery quantities from sale order. That is why procurement_jit needs to be
uninstalled from Apps or, which is perhaps a more preferred choice, going to
Inventory -> Configuration -> Settings and clicking the option "Manually or
based on automatic scheduler" under Reservation selection. This will uninstall
procurement_jit module.

When the previously mentioned part is in order, this module works properly.
To enable the automatic unreservation go to Sale settings via Sales ->
Configuration -> Settings and select Force Unreserve to always unreserve
deliveries created from sale orders.

Usage
=====
Install the module by going to Apps and search for the name of this module.

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Timo Kekäläinen <timo.kekalainen@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
