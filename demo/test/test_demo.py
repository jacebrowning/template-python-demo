#!/usr/bin/env python

"""Sample test module."""

import unittest

from demo import sample


class TestDemo(unittest.TestCase):

    """Sample test class."""

    def test_dependency_import(self):
        """Sample test method for dependencies."""
        try:
            import testpackage  # pylint: disable=W0612
            assert True
        except ImportError:
            self.fail("depenency not installed")

    def test_dependency_import_special(self):
        """Sample test method for special dependencies."""
        try:
            import newrelic_plugin_agent  # pylint: disable=W0612
            assert True
        except ImportError:
            self.fail("depenency not installed")

    def test_branch_coverage(self):
        """Sample test method for branch coverage."""
        self.assertEquals(sample.function(True), 'True')
        self.assertEquals(sample.function(False), 'False')
        self.assertEquals(sample.function(None), 'None')

    def test_another_function(self):
        """Verify another function works as expected."""
        self.assertTrue(sample.another_function("abc123"))
        self.assertFalse(sample.another_function(""))
