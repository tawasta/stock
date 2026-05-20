.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================================================
Stock Picking: Show 'Destination Location' in Operations List
=============================================================

* Enables destination location editing per stock move on the picking form.
* Intended for situations where you want to easily log e.g. multiple 
  internal transfers with different destination locations

Configuration
=============
* Consider installing stock_move_product_default_location if you also want the
  source location to be visible and editable

Usage
=====
* Open a picking form and adjust the visible columns in the Operations tab

Known issues / Roadmap
======================
* Other modules may affect how stock.move location_dest_id -field works. Test
  this module in a test environment first.


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
