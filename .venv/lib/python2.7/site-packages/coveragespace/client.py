"""API client functions."""

import time
import logging

import requests

from .cache import Cache


log = logging.getLogger(__name__)
cache = Cache()


def get(url, data):
    log.info("Getting %s: %s", url, data)

    response = cache.get(url, data)
    if response is None:
        for i in range(3):
            response = requests.put(url, data=data)
            if response.status_code == 500:
                time.sleep(i + 1)
                continue
            else:
                break
        cache.set(url, data, response)

    log.info("Response: %s", response)

    return response


def delete(url, data):
    log.info("Deleting %s: %s", url, data)

    for i in range(3):
        response = requests.delete(url, data=data)
        if response.status_code == 500:
            time.sleep(i + 1)
            continue
        else:
            break

    log.info("Response: %s", response)

    return response
