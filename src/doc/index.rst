.. Dunder documentation master file, created by
   sphinx-quickstart on Thu Oct 02 15:57:28 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Dunder v\ |version|
===================

Dunder is a small module which extracts `dunder`_ variables from Python
source files.

Example
=======

The following example demonstrates the functionality available in the module.

Using the following Python source file :file:`test.py` ::

    # -*- coding: utf-8 -*-

    # Copyright 2014 Joe Bloggs Inc.

    """Module docstring"""

    import datetime

    __all__ = ['a']

    __version__ = "0.1"
    __author__ = "Joe Bloggs <joe.bloggs@example.com>"
    __wally__ = 1
    __dave__ = 1.1
    __brian__ = (1, 2, 3)

    def a():
        __walter__ = 'dave'
	
Running the following code will extract the 'dunder' variables and present
them as a dictionary ::

    >>> import dunder
    >>> d = dunder.parse('test.py')
    >>> print(d['__version__'])
    0.1
    >>> print(d['__walter__'])
    dave

.. note::
  
   For lists and tuples only values of a single level are parsed correctly
   i.e. (1, 2) and [2, 's'] work but [1, [3, 5], 6] doesn't


License
=======

This module is licensed under the terms of the `Apache`_ V2.0 license.

Dependencies
============

Dunder has no external dependencies.

Installation
============

Installation can be performed by using the :command:`pip` command. ::

   pip install dunder 

Contact
=======
    
Simon Kennedy <sffjunkie+code@gmail.com>
    
Version History
===============

======== =======================================================================
Version  Description
======== =======================================================================
0.1.1    Use some `selfdogfooding`_ in :file:`setup.py`
-------- -----------------------------------------------------------------------
0.1      First release
======== =======================================================================

.. _Apache: http://www.opensource.org/licenses/apache2.0.php
.. _dunder: https://wiki.python.org/moin/DunderAlias
.. _selfdogfooding: http://indiewebcamp.com/selfdogfood
