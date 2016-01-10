"""Sample integration test module."""
# pylint: disable=no-self-use

import unittest

from demo import sample


class TestDemo(unittest.TestCase):

    """Sample integration test class."""

    def test_network_stuff(self):
        assert sample.function_with_network_stuff() is True

    def test_disk_stuff(self):
        assert sample.function_with_disk_stuff() is False
