.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=========================================================================
Change duplicate check to enable multiple adjustments for a same location
=========================================================================

stock_inventory -module does not support having several inventory adjustments
open for a same location, even when those adjustments would not have the
same products. This module was created to allow this, but not when those
adjustments contain some common products.

Configuration
=============
There is no need to configure anything

Usage
=====
Create several inventory adjustments with a same stock location to test
the behaviour of this module.

Known issues / Roadmap
======================
See that a user cannot bypass the new restrictions in the future.

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
