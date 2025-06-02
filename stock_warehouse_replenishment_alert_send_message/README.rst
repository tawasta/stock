.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=================================================================================
Send a message if Qty On Hand drops below its minimium quantity in replenishments
=================================================================================

Send a message for the responsible if Quantity drops below its minimium quantity in replenishments.

Configuration
=============
Check that products in replenishments have their respective responsible set
so that sending messages is possible.

Usage
=====
Go to Replenishments to see their Quantities on hand. If this quantity
drops below zero, the responsible of a product receives an alert message
about this.

Known issues / Roadmap
======================
This module works with onchange and it is possible that this won't always
trigger and therefore send a message.

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
