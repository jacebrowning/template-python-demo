"""Plugins to extract coverage data from various formats."""

import os

import coverage

from .base import BasePlugin


def get_coverage():
    """Find a matching coverage plugin and use it to extract coverage data."""
    cwd = os.getcwd()

    for cls in BasePlugin.__subclasses__():  # pylint: disable=no-member
        plugin = cls()
        if plugin.match(cwd):
            break
    else:
        raise RuntimeError("No coverage data found in the current directory.")

    percentage = plugin.run(cwd)

    return round(percentage, 1)


class CoveragePy(BasePlugin):
    """Coverage extracter for the coverage.py format."""

    def match(self, cwd):
        return '.coverage' in os.listdir(cwd)

    def run(self, cwd):
        os.chdir(cwd)

        cov = coverage.Coverage()
        cov.load()

        with open(os.devnull, 'w') as ignore:
            total = cov.report(file=ignore)

        return total
