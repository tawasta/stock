.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================================================
Expiration Date of lot can be set when receiving a product
==========================================================

::

    In Receipts, use the new field, expiration_date_lot, to set an expiration date
    to expiration_date -field on stock.move.line and also to the lot.

    This functionality overrides the restrictions that an expiration date of existing lots
    cannot be changed when receiving a product.

Configuration
=============
::

    None needed at the moment

Usage
=====
::

    Go to a receipt to receive a product that has serial tracking enabled.
    Select an existing lot and change the expiration date when choosing
    this lot in the normal lot dialog window.

Known issues / Roadmap
======================
::

    Using this module should not be too dangerous because users themselves
    define the expiration date for lots. This can be done anyway in the
    lot form view.

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
