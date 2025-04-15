.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============================================================
Stock Picking: Dropshipping Move Description from Product Name
==============================================================

* Do not ever use product's 'description' field as move description 
  when handling a drop shipping picking. Instead show just the 
  product name.
* Intended to ensure no confidential info accidentally ends up
  on e.g. drop shipping delivery slip prints

Configuration
=============
* None needed

Usage
=====
* Create a drop shipping picking. Print a delivery slip. Products'
  descriptions do not contain anything from products' Internal Notes
  section.

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@futural.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
