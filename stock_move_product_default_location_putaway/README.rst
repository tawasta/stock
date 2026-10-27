.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============================================================
Sync Putaway arrives in location with product default location
==============================================================

::

    When product default location is changed, also change the same
    used arrives in location in product putaway rules according to the
    new product default location.

Configuration
=============
::

    Go to Inventory settings to set Default arrives in location
    for created Putaway rules. These rules are created for
    products with a default stock move location.

Usage
=====
::

    Change or set default stock move location for a product.  Also the
    scheduled action "Set or Create Putaway with default Product location"
    can be used to create putaway rules or set arrives in location.

Known issues / Roadmap
======================
::

    This module does not change Odoo logic, but helps updating and creating
    putaway rules.

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
