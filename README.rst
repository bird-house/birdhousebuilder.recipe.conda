*****************************
birdhousebuilder.recipe.conda
*****************************

.. image:: https://travis-ci.org/bird-house/birdhousebuilder.recipe.conda.svg?branch=master
   :target: https://travis-ci.org/bird-house/birdhousebuilder.recipe.conda
   :alt: Travis Build


Introduction
************

``birdhousebuilder.recipe.conda`` is a `Buildout`_ recipe to install `Anaconda`_ packages. This recipe is used by the `Birdhouse`_ project. 

.. _`Buildout`: http://buildout.org/
.. _`Anaconda`: http://www.continuum.io/
.. _`Birdhouse`: http://bird-house.github.io/

Usage
*****

The recipe requires that Anaconda is already installed. You can use the buildout option ``anaconda-home`` to set the prefix for the anaconda installation. You can also use the recipe option ``prefix`` to set the conda prefix. Otherwise the environment variable ``CONDA_PREFIX`` (variable is set when activating a conda environment) is used as conda prefix. 


Supported options
=================

This recipe supports the following options:

**anaconda-home**
   Buildout option pointing to the root folder of the Anaconda installation. Default: ``$HOME/anaconda``.

**conda-channels**
   Buildout option (optional) with channels of conda packages. Default: defaults

**conda-offline**
   Buildout option (optional) to set conda offline mode. It has no effect when buildout is already in offline mode. Default: false

**channel-priority**
   Buildout option (optional) to set channel priority in conda install. Default: true

**prefix**
  Path to the conda prefix (optional). If not given then ``CONDA_PREFIX`` or anaconda-home will be used.
  
**pkgs**
   A list of packages to install, separated by space.

**channels**
   A list of space separated conda channels (optional). These channels are merged with conda-channels option. Default: defaults.

**override-channels**
   If True then default channels from ``~/.condarc`` are ignored (optional). Default. true.

**no-pin**
   If True then conda pinned file is ignored (optional). Default: false.

**env**
   Name of conda environment used for installation (optional). If environment is missing then packages are installed in the active environment.

**default-pkgs**
   A list of packages to install when creating a conda environment separated by space (optional). Default: ``python``

**pip-pkgs**
   A list of packages which are installed by pip into the conda enviroment (optional).

.. note::

   If buildout is run in offline mode no network connection will be establish and conda packages will not be installed.

.. note::

   If buildout is run in ``newest=false`` mode then conda dependencies are not updated.


Example usage
=============

The following example ``buildout.cfg`` installs the packages in the active conda environment.

.. code-block:: sh

  [buildout]
  parts = conda

  [conda]
  recipe = birdhousebuilder.recipe.conda
  pkgs = lxml owslib
  channels = defaults birdhouse


