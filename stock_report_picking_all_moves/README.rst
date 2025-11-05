.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================================
Stock Picking PDF Report - Show all stock moves
===============================================

This module adds another **Stock Picking Report** and includes an alternative report action
that shows Stock Moves related to a picking instead of the reserved moves (stock.move.line).

The implementation introduces a new `ir.actions.report` entry and a wrapper
template that calls the core `stock.report_picking` QWeb template with
an additional context variable `all_moves=True`.

When this variable is active, the core report hides its original
`move_line_ids_without_package` loop and instead iterates over
all `move_ids` belonging to the picking.

Configuration
=============
None needed

Usage
=====
1. Install this module.
2. Open any Stock Picking document.
3. Click **Print → Picking Operations (All Moves)** to print the new version.

Known issues / Roadmap
======================
The module extends some t-if conditions in the original picking PDF print.
Take notice of these changes.

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>
* Timo Kekäläinen <timo.kekalainen@tawasta.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
