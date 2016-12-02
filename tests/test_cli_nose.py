"""Sample integration test module using nose."""
# pylint: disable=no-self-use,missing-docstring

import unittest

from click.testing import CliRunner

from demo.cli import main


class TestDemo(unittest.TestCase):
    """Sample integration test class."""

    def test_conversion(self):
        runner = CliRunner()
        result = runner.invoke(main, ['42'])

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, "12.80165\n")
