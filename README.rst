*****************************
birdhousebuilder.recipe.conda
*****************************

.. contents::

Introduction
************

``birdhousebuilder.recipe.conda`` is a `Buildout`_ recipe to install `Anaconda`_ packages.

.. _`Buildout`: http://buildout.org/
.. _`Anaconda`: http://www.continuum.io/

Usage
*****

The recipe requires that Anaconda is already installed. It assumes that Anaconda is installed at the default location in your home directory ``~/anaconda``. Otherwise you need to set the Buildout option ``anaconda-home``.


Supported options
=================

This recipe supports the following options:

``anaconda-home``
   Buildout option with the root folder of the Anaconda installation. Default: ``$HOME/anaconda``.

``conda-channels``
   Buildout option (optional) with additional channels of conda packages. 
  
``pkgs``
   A list of pkgs to install separated by space.

``on-update``
   If set to false conda will not check for updates when running buildout update.

Example usage
=============

The following example ``buildout.cfg`` installs the conda packages lxml, nose and matplotlib::

  [buildout]
  parts = conda_pkgs

  anaconda-home = /home/myself/anaconda
  conda-channels = https://conda.binstar.org/myself

  [conda_pkgs]
  recipe = birdhousebuilder.recipe.conda
  pkgs = lxml nose matplotlib
  on-update = false

