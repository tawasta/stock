.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================
Stock: Product Labels with Barcode
==================================

* Adds new label type "Product Sticker: Product Barcode" to the Print Label wizard
  that prints a customized label with a name, barcode field contents as barcode,
  and barcode field contents as text

Configuration
=============
* None needed

Usage
=====
* Launch the Print Labels wizard from e.g. picking or product form view

Known issues / Roadmap
======================
* Currently always called in en_US to get english product names. Consider making this a
  configurable option
* Configured for a specific label printer - if sticker dimensions differ when using another printer,
  style changes are probably needed.

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@futural.fi>
* Timo Kekäläinen <timo.kekalainen@futural.fi>


Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
