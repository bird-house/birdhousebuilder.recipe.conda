Changes
*******

0.3.5 (2016-10-12)
==================

* added buildout option channel-priority.
* fixed order of channels.

0.3.4 (2016-10-10)
==================

* added buildout option conda-offline (#8).

0.3.3 (2016-08-05)
==================

* fixed: added missing CalledProcessError import

0.3.2 (2016-07-11)
==================

* catch conda exception (#7).

0.3.1 (2016-06-30)
==================

* using ``CONDA_PREFIX``.

0.3.0 (2016-06-28)
==================

* added option no-pin and override-channels.
* sets conda env-path and prefix in options. 
* enabled travis build.
* removed unused as_bool and makedirs functions.
* using bool_option from zc.buildout.
* using conda offline mode.
* install pip packages.
* added prefix option.
* using ``CONDA_ENV_PATH``.

0.2.7 (2016-04-15)
==================

* removed default ioos conda channel.

0.2.6 (2015-12-15)
==================

* added default ioos conda channel.

0.2.5 (2015-09-21)
==================

* use buildout offline option ... don't establish internet connection when enabled.

0.2.4 (2015-08-05)
==================

* use CONDA_ENVS_DIR to overwrite base dir of conda environments. 

0.2.2 (2015-02-25)
==================

* sets buildout:prefix option as installation default directory for birdhouse.

0.2.1 (2015-02-24)
==================

* setting ``anaconda-home`` with environment variable ``$ANACONDA_HOME``.
* separation of install prefix and anaconda-home.

0.2.0 (2015-02-23)
==================

* conda environments can be created now.
* added channels option.

0.1.4 (2015-01-09)
==================

* added https://conda.binstar.org/birdhouse to default channels.

0.1.3 (2015-01-08)
==================

* added https://conda.binstar.org/scitools to default channels.

0.1.2 (2014-12-02)
==================

* added on on-update buildout option. 

0.1.1 (2014-07-31)
==================

* Updated documentation.

0.1.0 (2014-07-10)
==================

* Initial Release.
