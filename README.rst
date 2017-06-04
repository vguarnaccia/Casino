======
Casino
======

.. image:: https://travis-ci.org/vguarnaccia/Casino.svg?branch=master
    :target: https://travis-ci.org/vguarnaccia/Casino

.. image:: https://coveralls.io/repos/github/vguarnaccia/Casino/badge.svg?branch=master
    :target: https://coveralls.io/github/vguarnaccia/Casino?branch=master

This package is and exercise in object oriented design, unittest, and documentation inspired heavily by Steven F. Lott's `Building Skills in Object-Oriented Design. <http://buildingskills.itmaybeahack.com/oodesign.html>`_ I also intend to use it as template to use as an example of setting up a package. This README should be considered a **stub** for now.

.. todo:
    Expand synopsis

==================
How to Get Started
==================

These instructions will show you how to setup and use *Casino*.

Prerequisites
==============

You will need python version 3. No other modules are required to run the game but `Sphinx <sphinx-doc.org>`_ is required for generating docs and `Coverage <coverage.readthedocs.io>`_ is useful for testing.

Installation
============

Just use pip::
    
    pip install git+https://github.com/vguarnaccia/Casino/

Examples
========

.. todo 
    Add some code examples.

Testing
=======

Tests are written using the unittest, or doctests modules. Unittests should enfoce 100% test coverage on all functions and classes. They can be executed as a script::

    python -m casino.test

Or, better yet::

    coverage run -m casino.test # you can now review coverage reports

Acknowledgements
================

- Code inspired by Steven F. Lott's `Building Skills in Object-Oriented Design. <http://buildingskills.itmaybeahack.com/oodesign.html>`_
- Coding style from `Google Style Guide. <google.github.io/styleguide/pyguide.html>`_
- `Docstring Style. <http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_

.. todo:
    add buttons for travis builds, python versions
    point to python.org for module names.
