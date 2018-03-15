==========================================
Doctests for birdhousebuidler.recipe.conda
==========================================

Simple example
==============

    >>> import os

Simple buildout.cfg
===================

Lets create a minimal `buildout.cfg` file::

  >>> write('buildout.cfg',
  ... '''
  ... [buildout]
  ... parts = conda
  ... offline = true
  ...
  ... [conda]
  ... recipe = birdhousebuilder.recipe.conda
  ... pks = yaml
  ... channels = defaults
  ... ''')
