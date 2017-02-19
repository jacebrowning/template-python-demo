"""Update project metrics on The Coverage Space.

Usage:
  coverage.space <owner/repo> <metric> [<value>] [--verbose] [--exit-code]
  coverage.space <owner/repo> --reset [--verbose]
  coverage.space (-h | --help)
  coverage.space (-V | --version)

Options:
  -h --help         Show this help screen.
  -V --version      Show the program version.
  -v --verbose      Always display the coverage metrics.
  -x --exit-code    Return non-zero exit code on failures.

"""

from __future__ import unicode_literals

import sys
import json
import logging

import six
from docopt import docopt
import colorama
from backports.shutil_get_terminal_size import get_terminal_size

from . import API, VERSION
from . import services, client
from .plugins import get_coverage


log = logging.getLogger(__name__)


def main():
    """Parse command-line arguments, configure logging, and run the program."""
    colorama.init(autoreset=True)
    arguments = docopt(__doc__, version=VERSION)

    slug = arguments['<owner/repo>']
    metric = arguments['<metric>']
    reset = arguments['--reset']
    value = arguments['<value>'] or (None if reset else get_coverage())
    verbose = arguments['--verbose']
    hardfail = arguments['--exit-code']

    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.WARNING,
        format="%(levelname)s: %(name)s: %(message)s",
    )

    success = run(slug, metric, value, reset, verbose, hardfail)

    if not success and hardfail:
        sys.exit(1)


def run(*args, **kwargs):
    """Run the program."""
    if services.detected():
        log.warning("Coverage check skipped when running on CI service")
        return True
    else:
        return call(*args, **kwargs)


def call(slug, metric, value, reset=False, verbose=False, hardfail=False):
    """Call the API and display errors."""
    url = "{}/{}".format(API, slug)
    data = {metric: value}
    if reset:
        response = client.delete(url, data)
    else:
        response = client.get(url, data)

    if response.status_code == 200:
        if verbose:
            display("coverage increased", response.json(), colorama.Fore.GREEN)
        return True

    elif response.status_code == 202:
        display("coverage reset", response.json(), colorama.Fore.BLUE)
        return True

    elif response.status_code == 422:
        color = colorama.Fore.RED if hardfail else colorama.Fore.YELLOW
        data = response.json()
        data['help'] = \
            "To reset metrics, run: coverage.space {} --reset".format(slug)
        display("coverage decreased", data, color)
        return False

    else:
        try:
            data = response.json()
            display("coverage unknown", data, colorama.Fore.RED)
        except (TypeError, ValueError) as exc:
            data = response.data.decode('utf-8')
            log.error("%s\n\nwhen decoding response:\n\n%s\n", exc, data)
        return False


def display(title, data, color=""):
    """Write colored text to the console."""
    color += colorama.Style.BRIGHT
    width, _ = get_terminal_size()
    six.print_(color + "{0:=^{1}}".format(' ' + title + ' ', width))
    six.print_(color + json.dumps(data, indent=4))
    six.print_(color + '=' * width)
