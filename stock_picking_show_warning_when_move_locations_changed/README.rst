.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================================================
Stock Picking: Show Warning When Move Locations Change
======================================================

* Warn the user about changing picking-level locations if 
  move-level locations have already been changed
* Intended for situations where you have modules installed
  that allow move-level changing of the locations and
  the user might accidentally overwrite them with picking's 
  location fields' onchange.
* Modules this might be useful with are at least:

  * stock_picking_show_move_destination_location_column
  * stock_move_product_default_location

Configuration
=============
* None needed

Usage
=====
* Open a picking form and adjust the locations on the individual
  moves on the Operations tab. Warning message shows up under
  the picking's location fields

Known issues / Roadmap
======================
* None

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
