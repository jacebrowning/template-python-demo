"""Utilities to detect when this program is running on external services."""

import os


CONTINUOUS_INTEGRATION = [

    # General
    'CI',
    'CONTINUOUS_INTEGRATION',

    # Travis CI
    'TRAVIS',

    # Appveyor
    'APPVEYOR',

    # CircleCI
    'CIRCLECI',

]


def detected():
    return any(name in CONTINUOUS_INTEGRATION for name in os.environ)
