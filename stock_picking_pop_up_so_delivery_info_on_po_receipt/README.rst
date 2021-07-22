.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================================
Show Pop up on PO receipt that was created from SO
==================================================

* Pop up appears on Purchase Order receipt validation if that
  Purchase Order was created from Sale Order, which has a delivery.

Configuration
=============
* No special configuration needed

Usage
=====
* Go to Apps to install this module. Create a sale order with a product that
  has Make To Order and Buy routes, which will create a purchase order. Validate
  that purchase order and finish its delivery. This module's pop up should
  appear only then.

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
