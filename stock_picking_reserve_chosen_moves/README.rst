.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================================
Reserve individual moves on a picking
=====================================

Select manually the moves to be reserved on deliveries. Press
Reserve-button to reserve an individual move. The button will
be hidden after pressing the button, but only if reserving a
move is possible. Clicking on "Check Availability" button goes
through all the moves of a picking and marks them as reserved,
if a reservation was possible. All the moves are reserved then
if possible and their respective Reserve-button is hidden also.

Configuration
=============
* This module works best with stock_picking_unreserve_automatically module,
  which would automatically unreserve created pickings. So it is recommended
  to also use that module.

Usage
=====
* Go to Apps and install the module.

Known issues / Roadmap
======================
\-

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
