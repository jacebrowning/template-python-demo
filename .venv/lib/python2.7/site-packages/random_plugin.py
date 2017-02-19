from itertools import groupby
from random import Random
import time


# command line options
def pytest_addoption(parser):
    group = parser.getgroup("random", "randomize the tests to be run")
    group._addoption('--random',
        action="store_true",
        dest="random",
        default=False,
        help="randomize the tests to be run. defaults to False.")
    group._addoption('--random-group',
        action="store_true",
        dest="random_group",
        default=False,
        help="group by fixtures to avoid multiple setUp/tearDown calls. defaults to False.")
    group._addoption('--random-seed',
        action="store",
        dest="random_seed",
        type=int,
        default=int(time.time() * 256),
        help="the seed to use for randomization if you need to repeat a run.")


def pytest_report_header(config):
    if config.option.random:
        return "Tests are shuffled using seed number %d." % config.option.random_seed


def pytest_collection_modifyitems(session, config, items):
    """ called after collection has been performed, may filter or re-order
    the items in-place."""
    if not config.option.random:
        return
    random = Random()
    random.seed(config.option.random_seed)
    random.shuffle(items)
    if not config.option.random_group:
        return
    groups = {}
    _fixtures_getter = lambda x: tuple(getattr(x, 'fixturenames', ()))
    for k, g in groupby(items, _fixtures_getter):
        groups.setdefault(k, []).extend(g)
    items[:] = sum(groups.values(), [])
