.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================================
Stock warning when shipping product
===================================

Warns or completely blocks user from creating a new stock.picking record with certain product.

Configuration
=============
\-

Usage
=====
- To enable this feature, user must toggle 'Sale Warnings' boolean field from the sale settings.
- User is then able to set the stock_line_warn and stock_line_warn_msg fields on product.template
  and product.product records on Sales page.
- The fields on both product.template and product.product should automatically
  copy the values from each other if the user sets the values for either one of the records.
- Based on the stock_line_warn selection the adding of the product is either blocked or the user is warned
  about adding the product on the record.

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Kalle Rantalainen <kalle.rantalainen@tawasta.fi>

Maintainer
----------

.. image:: https://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: https://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
