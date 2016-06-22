# -*- coding: utf-8 -*-
"""
Doctest runner for 'birdhousebuilder.recipe.conda'.
"""

import os
from doctest import DocFileSuite
from doctest import ELLIPSIS
from doctest import NORMALIZE_WHITESPACE
from doctest import REPORT_UDIFF
from zc.buildout.testing import buildoutSetUp
from zc.buildout.testing import buildoutTearDown
from zc.buildout.testing import install_develop

def setUp(test):
    buildoutSetUp(test)
    # Work around "Not Found" messages on Buildout 2
    del os.environ['buildout-testing-index-url']
    test.globs['buildout'] += ' -No'

    install_develop('birdhousebuilder.recipe.conda', test)

def test_suite():
    return DocFileSuite(
        '../README.txt',
        setUp=setUp, tearDown=buildoutTearDown,
        optionflags=ELLIPSIS | NORMALIZE_WHITESPACE | REPORT_UDIFF)

