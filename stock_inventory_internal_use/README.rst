.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============================
Stock Inventory internal use
============================

::

    Inventory view meant for internal use. This view has only one
    purpose: to decrease stock quantity one by one with -1 button.
    After quantity has been set, a user clicks on Apply button or
    Clear button to cancel the quantity change.

Configuration
=============
::

    No configuration is necessary

Usage
=====
::

    Go to Internal Use menu under Inventory. Then press -1 button
    on a chosen stock quant. Each click decreases the quantity to
    be applied by one and this can be seen from Difference column.

    After quantity has been set, the user clicks either Apply or
    Clear button. Apply button sets the new assigned product quantity
    to stock quant. Clear button cancels the process.

Known issues / Roadmap
======================
::

    This module is for simple use and no issues are expected.
    But understand that inventory_quantity -field is manipulated
    with operation_quantities_decrease_internal() -method. In
    case of problems check how inventory_quantity -field is being
    used by other modules.

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
