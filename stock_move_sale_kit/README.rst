.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

==================================================
Stock Move Sale Kit – information on SO deliveries
==================================================

* Adds sale packages to stock move lines
* Creates barcodes from sale kit

Configuration
=============
No configuration is needed. A user just needs to use the module.

Usage
=====
Go to manufacturing section and select or create a BoM which
is of Kit type. Then create a sale order and confirm it with
this Kit. Created deliveries have information about the kit
added to its moves.

Known issues / Roadmap
======================
The module modifies _get_stock_move_values() -function of stock.rule model
and adds sale_line_id -field information to deliveries that are possibly
created with customized routings. This way Kit information is copied to
those deliveries also.

Credits
=======

Contributors
------------

* Miika Nissi <miika.nissi@tawasta.fi>
* Timo Kekäläinen <timo.kekalainen@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
        :alt: Oy Tawasta OS Technologies Ltd.
        :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
