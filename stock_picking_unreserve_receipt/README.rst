.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================================
Configure to automatically unreserve receipts
=============================================

Select a picking type that handles receipts and choose "Unreserve receipt" field
as True. After that, pickings created from purchases will be unreserved automatically.

Configuration
=============
None

Usage
=====
Use a picking type to change how receipt type of pickings are reserved

Known issues / Roadmap
======================
This module modifies _create_picking() function

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
