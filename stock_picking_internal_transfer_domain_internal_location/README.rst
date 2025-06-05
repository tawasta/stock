.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================================================
Use Internal location as domain for Internal transfers
======================================================

Use Internal location as domain for Internal transfers

Configuration
=============
\-

Usage
=====
\-

Known issues / Roadmap
======================
The code does not work for non-internal transfers. Not sure
how to fix the issue, but I left defaut_get() and view changes
just in case someone can make it work. Issue is that the domain
change affects both location_id fields in the views.

default_get() does work though.

Credits
=======

Contributors
------------

* Timo Kekäläinen <timo.kekalainen@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
