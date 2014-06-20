*****************************
birdhousebuilder.recipe.conda
*****************************

.. contents::

Introduction
************

``birdhousebuilder.recipe.conda`` is a `Buildout`_ recipe to install conda packages.

.. _`Buildout`: http://buildout.org/

Usage
*****

Supported options
=================

The recipe supports the following options:

``on_install``
    true if the commands must run on install

``on_update``
    true if the commands must run on update

``pkgs``
    a list of pkgs to install separated by space

Example usage
=============

We need a config file::

  >>> cfg = """
  ... [buildout]
  ... parts = cmds
  ...
  ... [cmds]
  ... recipe = birdhousebuilder.recipe.conda
  ... on_install=true
  ... pkgs= %s
  ... """

  >>> pkgs = 'conda numpy'
  >>> write(sample_buildout, 'buildout.cfg', cfg % pkgs)

