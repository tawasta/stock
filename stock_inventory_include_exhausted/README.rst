.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================================
Stock Inventory Adjustment: Include Exhausted
=============================================

* Option to automatically add rows for exhausted products when doing inventory
* Intended to mimic the behaviour of the "Exhausted" checkbox found in earlier
  Odoo versions, making it so that the user does not have to manually add rows
  for all exhausted products in the Adjustments view.

Configuration
=============
* None needed

Usage
=====
* Create a new Inventory Adjustment Group
* Toggle the "Include Exhausted" option on and begin the inventory
* Click Adjustments action button. Lines are created also for products without any stock

Known issues / Roadmap
======================
* Adjusting multiple locations inventory simultaneously is not currently supported
* Lot/Serial Number selection is not currently supported

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
