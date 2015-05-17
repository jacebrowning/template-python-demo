"""Sample integration test module."""

import unittest

from demo import sample


class TestDemo(unittest.TestCase):

    """Sample integration test class."""

    def test_io_stuff(self):
        assert sample.function_that_does_io() is True
