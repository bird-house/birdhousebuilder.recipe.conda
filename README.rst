*****************************
birdhousebuilder.recipe.conda
*****************************

.. contents::

Introduction
************

``birdhousebuilder.recipe.conda`` is a `Buildout`_ recipe to install `Anaconda`_ packages. This recipe is used by the `Birdhouse`_ project. 

.. _`Buildout`: http://buildout.org/
.. _`Anaconda`: http://www.continuum.io/
.. _`Birdhouse`: http://bird-house.github.io/

Usage
*****

The recipe requires that Anaconda is already installed. It assumes that the default Anaconda location is in your home directory ``~/anaconda``. Otherwise you need to set the ``ANACONDA_HOME`` environment variable or the Buildout option ``anaconda-home``.


Supported options
=================

This recipe supports the following options:

``anaconda-home``
   Buildout option with the root folder of the Anaconda installation. Default: ``$HOME/anaconda``.
   The default location can also be set with the environment variable ``ANACONDA_HOME``. Example::

     export ANACONDA_HOME=/opt/anaconda

   Search priority is:

   1. ``anaconda-home`` in ``buildout.cfg``
   2. ``$ANACONDA_HOME``
   3. ``$HOME/anaconda``
  
``conda-channels``
   Buildout option (optional) with additional channels of conda packages. 
  
``pkgs``
   A list of packages to install separated by space.

``channels``
   A list of space separated conda channels (optional). These channels are merged with conda-channels option.

``env``
   Name of conda environment used for installation (optional). If environment is missing then all packages are installed in the anaconda root environment (``anaconda-home``).

``default-pkgs``
   A list of packages to install when creating environment separated by space (optional). Default: ``python``

``on-update``
   If set to false conda will not check for updates when running buildout update. Default: ``false``.

Example usage
=============

The following example ``buildout.cfg`` installs the conda packages lxml, nose and matplotlib::

  [buildout]
  parts = conda_pkgs

  anaconda-home = /opt/anaconda
  conda-channels = birdhouse

  [conda_pkgs]
  recipe = birdhousebuilder.recipe.conda
  pkgs = lxml nose matplotlib owslib
  channels = birdhouse asmeurer
  env = mytest
  default-pkgs = python
  on-update = false

