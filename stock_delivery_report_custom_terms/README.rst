.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============================
Custom Delivery Report Terms
============================

This module allows configuring the terminology used in the stock delivery
slip report instead of relying on hardcoded values.

By default, Odoo uses the terms:

* Ordered
* Delivered

This module makes those labels configurable from system settings and supports
standard Odoo translations.

Configuration
=============

Go to:

* Inventory -> Configuration -> Settings

Under **Delivery Report Terms**, configure:

* Ordered term
* Delivered term

The configured values are company-specific.

Translations can be maintained using Odoo's standard translation framework.

Usage
=====

After configuration, the delivery slip report will display the configured
terms instead of the default hardcoded labels.

The following report headers are affected:

* Ordered
* Delivered

Both open and completed delivery slip reports use the configured values.

Known issues / Roadmap
======================

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
