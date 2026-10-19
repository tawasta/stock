.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============
Stock Warnings
==============

* Adds the field *Stock Warning Level* to the partner, next to the core
  field *Instructions on the Stock Operations*

  * Warning

    * Show the instructions underneath the field on the stock picking only
      (core behavior)

  * Popup Warning

    * Show a popup with the instructions when the partner is chosen on the
      stock picking, in addition to underneath the field

  * Blocking Warning

    * Prevent changing the partner of an existing stock picking to this
      partner

* The popup and the blocking are provided by the module partner_warnings

Configuration
=============
\-

Usage
=====

* User

  * Install module
  * Go to Settings -> Inventory

    * Check "Stock Warnings" (a warning can be set on a partner)

  * Set the instructions and the warning level on the partner form

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
