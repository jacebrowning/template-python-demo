"""Base classes."""

from abc import ABCMeta, abstractmethod

from six import with_metaclass


class BasePlugin(with_metaclass(ABCMeta)):  # pragma: no cover (abstract class)
    """Base class for coverage plugins."""

    @abstractmethod
    def match(self, cwd):
        """Determine if the current directory contains coverage data.

        :return bool: Indicates the current directory can be processesed.

        """

    @abstractmethod
    def run(self, cwd):
        """Extract the coverage data from the current directory.

        :return float: Percentange of lines covered.

        """
