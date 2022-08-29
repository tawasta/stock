.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================================================
Stock Move pivot view - Group by SH product tags
================================================

sh_product_tag_ids values for Stock Moves are assignd automatically upon
a stock move record creation. This module has a cron, which can be used
to compute tag-values for old stock move records. Use the module's grouping
feature in the stock move pivot view.

Configuration
=============
OCA's sh_product_variant_tags module needs to be installed to use this
module.

Usage
=====
Install the module from Apps.

Known issues / Roadmap
======================
Note that stock move's sh_product_tag_ids field is a computed field and it
stores only the first value from stock moves's product's sh_product_tag_ids
field. This is because product's sh_product_tag_ids field is a many2many field,
which is rather bothersome to use to group things.

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
