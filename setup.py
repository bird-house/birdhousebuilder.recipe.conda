# -*- coding: utf-8 -*-
"""
This module contains the tool of collective.recipe.cmd
"""
from setuptools import find_packages
from setuptools import setup

name = 'birdhousebuilder.recipe.conda'

version = '0.3.4'
description = 'A Buildout recipe to install conda packages'
long_description = (
    open('README.rst').read() + '\n' +
    open('AUTHORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

entry_points = '''
[zc.buildout]
default = %(name)s:Recipe
[zc.buildout.uninstall]
default = %(name)s:uninstall
''' % globals()

reqs = ['setuptools', 'zc.buildout', 'pyyaml']
tests_reqs = ['zc.buildout', 'zope.testing']

setup(name=name,
      version=version,
      description=description,
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Framework :: Buildout',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'License :: OSI Approved :: BSD License',
      ],
      keywords='buildout recipe conda anaconda birdhouse',
      author='Birdhouse',
      author_email="wps-dev at dkrz.de",
      url='https://github.com/bird-house/birdhousebuilder.recipe.conda',
      license='Apache License 2',
      install_requires = reqs,
      extras_require = dict(tests=tests_reqs),
      entry_points = entry_points,
      packages = find_packages(exclude=['ez_setup']),
      namespace_packages = ['birdhousebuilder', 'birdhousebuilder.recipe'],
      include_package_data = True,
      zip_safe = False,
      )
