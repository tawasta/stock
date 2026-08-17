.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================================
Percentage update in stock valuation
====================================

Select a percentage on a product category to update price with this percentage
when the average cost valuation is recomputed.

rule_tip -field gives an example how the new price would change with
the set percentage.

Configuration
=============
Purchases need to be enable to use this module.

Important: Use Average cost for a product category!

Usage
=====
Select a percentage for a product category. Then buy a product from this
category and receive the product. The cost price of the product has been
changed by the percentage value.

Technical notes
================
Odoo 19 recomputes the average cost (``standard_price``) of a product in a
single batch pass (``product.product._update_standard_price()`` /
``_run_average_batch()``) instead of the per-move calculation used in
Odoo 17. This module lets core compute and write the real average cost
first, then applies the category's percentage on top of that value for
products using the "average" costing method, instead of re-implementing
the average cost calculation itself.

Known issues / Roadmap
======================
None known

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
