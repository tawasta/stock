.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================================
Percentage update in stock valuation
====================================

::

    Select a percentage on a product category to update price with this percentage
    when the average cost valuation is recomputed.

    rule_tip -field gives an example how the new price would change with
    the set percentage.

Configuration
=============
::

    Purchases need to be enable to use this module.

    Important: Use Average cost for a product category!

Usage
=====
::

    Select a percentage for a product category. Then buy a product from this
    category and receive the product. The cost price of the product has been
    changed by the percentage value.

Known issues / Roadmap
======================
::

    _set_value() method from stock_account module is modified directly in order
    not to disturb inheritance of other modules. The modified method has only
    percentage update inserted into it. This sets the stock valuation of a product.
    Check how this modifition is done to understand it correctly.

    _action_done() method from the same stock_account module is modified to update
    the cost of a product with an added percentage value.

Credits
=======

Contributors
------------

* Timo Kekäläinen <timo.kekalainen@tawasta.fi>
* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
