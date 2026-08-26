.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================================================================
Quantity Decimals Precision on Picking and Delivery Slip reports
================================================================

* Change the number of decimals shown on Stock reports' product quantities

Configuration
=============
* Stock reports' decimals precision of product quantities can be set by going
  to Inventory --> Configuration --> Settings and changing the value under the
  stock_report_decimal_precision-field. The integer represents the number of
  decimals shown on product quantities.

* 14 version adds a new decimal precision: "Company Precision". Use it in
  t-options if needed.

Usage
=====
* Install the module from Apps

Known issues / Roadmap
======================
* During port from v17 to v19 some of the xpath expressions were changed to 
match the new report structure. 

Credits
=======

Contributors
------------

* Timo Kekäläinen <timo.kekalainen@futural.fi>
* Kalle Rantalainen <kalle.rantalainen@futural.fi>
* Timo Talvitie <timo.talvitie@futural.fi>
* Joonas Lahtinen <joonas.lahtinen@futural.fi>


Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy

