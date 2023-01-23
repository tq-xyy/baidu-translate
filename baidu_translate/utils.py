import functools
import time

import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

session = requests.Session()


def environment(fn):
    _cache = None
    _cache_time = None

    def cache(data, refresh_time):
        nonlocal _cache, _cache_time
        if not _cache or (time.time() - _cache_time >= refresh_time):
            _cache = data
            _cache_time = time.time()
        return _cache

    def retry(fn, times):
        errors = None
        for _ in range(times):
            try:
                return fn()
            except Exception as err:
                errors = err
        raise errors

    @functools.wraps(fn)
    def wrapper():
        return cache(retry(fn, 5), 30)
    return wrapper
