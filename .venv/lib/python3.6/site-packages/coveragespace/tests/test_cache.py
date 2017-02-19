# pylint: disable=missing-docstring,unused-variable,unused-argument,expression-not-assigned,singleton-comparison

import os

import pytest
from expecter import expect

from coveragespace.cache import Cache


def describe_cache():

    @pytest.fixture
    def cache():
        return Cache()

    @pytest.fixture
    def cache_empty(cache):
        # pylint: disable=protected-access
        cache._data.clear()
        return cache

    @pytest.fixture
    def cache_missing(cache_empty):
        try:
            os.remove(Cache.PATH)
        except OSError:
            pass
        return cache_empty

    @pytest.fixture
    def cache_corrupt(cache):
        # pylint: disable=protected-access
        cache._data = "corrupt"
        cache._store()
        return cache

    def describe_init():

        def it_loads_previous_results(cache_empty):
            cache_empty.set("url", {}, "previous")

            cache = Cache()
            expect(cache.get("url", {})) == "previous"

        def it_handles_missing_cache_files(cache_missing):
            expect(Cache().get("url", {})) == None

        def it_handles_corrupt_cache_files(cache_corrupt):
            expect(Cache().get("url", {})) == None

    def describe_get():

        def it_hits_with_existing_data(cache_empty):
            cache = cache_empty
            cache.set("url", {}, "existing")

            expect(cache.get("url", {})) == "existing"

        def it_misses_with_no_data(cache_empty):
            expect(cache_empty.get("url", {})) == None
