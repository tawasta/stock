.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================================================
Default location for products to be used with stock moves
=========================================================

Move a product in a picking using its default location. This location
overrides the source location of a stock move. Then this is from where
a product is moved to its destination location.

Configuration
=============
Configure the default location for a product

Usage
=====
Create a picking and validate a move with a product that has a default
location which is a different location than the source location used in
a picking.

Known issues / Roadmap
======================
Other modules may affect how stock.move location_id -field works. Test
this module in a test environment.

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
