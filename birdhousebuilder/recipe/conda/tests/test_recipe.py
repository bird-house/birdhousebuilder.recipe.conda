# -*- coding: utf-8 -*-
"""
Doctest runner for 'birdhousebuilder.recipe.conda'.
"""

import os
import unittest
import zc.buildout.testing


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


def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(RecipeTests),
        ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
