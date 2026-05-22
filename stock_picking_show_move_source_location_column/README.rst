.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================================================
Stock Picking: Show 'Source Location' in Operations List
========================================================

* Enables source location editing per stock move on the picking form.
* Intended for situations where you want to easily log e.g. multiple
  internal transfers with different source locations

Configuration
=============
* Store products in different stock locations to transfer them per line
  in pickings

Usage
=====
* Open a picking form and adjust the visible columns in the Operations tab

Known issues / Roadmap
======================
* Other modules may affect how stock.move location_id -field works. Test
  this module in a test environment first.

Credits
=======

Contributors
------------

* Timo Kekäläinen <timo.kekalainen@tawasta.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
