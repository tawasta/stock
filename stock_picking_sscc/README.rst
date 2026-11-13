.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================
SSCC for stock picking
======================

::

    Assign SSCC value, Serial Shipping Container Code, to a created picking.
    Its extension digit, GS1 company prefix, Serial number and check digit
    has been taken into account when assigning a new SSCC value.

Configuration
=============
::

    Go to Inventory settings to set a speficif extension digit and
    GS1 company prefix to SSCC value. Also check SSCC Sequence in
    ir.sequence records found in Sequences from Settings. Change
    its number_next value to be something reasonable.

Usage
=====
::

    Create a new stock picking to see how the SSCC value has been assigned
    to it.

Known issues / Roadmap
======================
::

    SSCC field works separately from other functions.

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
