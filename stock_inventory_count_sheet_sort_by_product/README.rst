.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================================================================
Inventory Count Sheet – sort quants by their product _order -attribute
======================================================================

Count Sheet is not normally ordered by products' direct _order -attribute.
This module makes it easier to do inventory by showing products in the
same order as they appear in the stock quant view of inventory.

Configuration
=============
The module only uses stock module as its dependency, but this also
works with stock_inventory module.

Usage
=====
Go to inventory adjustments are print out Count Sheet. Its order has
been changed after the installation of this module.

Known issues / Roadmap
======================
The order of quants should be the same it is defined in _order attribute
of product.product model.

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
