# -*- coding: utf-8 -*-
"""
Doctest runner for 'birdhousebuilder.recipe.conda'.
"""

import os
import doctest
import unittest
import zc.buildout.testing

from zope.testing import renormalizing

optionflags = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE |
               doctest.REPORT_UDIFF |
               doctest.REPORT_ONLY_FIRST_FAILURE)

checker = renormalizing.RENormalizing([
        zc.buildout.testing.normalize_path,
        ])


class RecipeTests(unittest.TestCase):

    def setUp(self):
        buildout = zc.buildout.testing.Buildout()
        buildout['buildout']['offline'] = 'true'
        options = dict(pkgs='yaml')
        import birdhousebuilder.recipe.conda
        self.recipe = birdhousebuilder.recipe.conda.Recipe(
            buildout, name='conda', options=options)

    def tearDown(self):
        pass

    def test_install(self):
        self.assertEqual(self.recipe.install(), ())


def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    # Install the recipe in develop mode
    zc.buildout.testing.install_develop('birdhousebuilder.recipe.conda', test)
    # Install any other recipes that should be available in the tests
    zc.buildout.testing.install('zope.testing', test)


def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(RecipeTests),
        doctest.DocFileSuite(
            'README.rst',
            setUp=setUp,
            tearDown=zc.buildout.testing.buildoutTearDown,
            optionflags=optionflags,
            checker=checker),
        ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
