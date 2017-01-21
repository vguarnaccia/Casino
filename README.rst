======
Casino
======

This package is and exercise in object oriented design, unittest, and documentation inspired heavily by Steven F. Lott's `Building Skills in Object-Oriented Design. <http://buildingskills.itmaybeahack.com/oodesign.html>`_ I also intend to use it as template to use as an example of setting up a package. This README should be considered a **stub** for now.

==================
How to Get Started
==================

These instructions will show you how to setup and use *Casino*.

Preprequisites
==============

You will need python version 3.x (TODO). No other modules are required but `Sphinx <sphinx-doc.org>`_ is required for generating docs and `Coverage <coverage.readthedocs.io>`_ is useful for testing.

Installation
============

Just use pip::
    
    pip install git+https://github.com/vguarnaccia/Casino/

Examples
========

TODO: Add some code examples.

Testing
=======

Tests are written using the unittest, or doctests modules (todo: link to python.org). They can be executed as a script::

    python -m casino.test

Or, better yet::

    coverage run -m casino.test # you can now review coverage reports
