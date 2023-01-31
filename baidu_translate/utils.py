import asyncio
import atexit
import functools
import time
import weakref
import threading

import aiohttp

DEFAULT_CONCURRENT = 1

# For threading safe
_lock_local = threading.local()

# Due to Baidu's limitations, we cannot submit many requests at once.
def max_request_lock() -> asyncio.Semaphore:
    if not hasattr(_lock_local, 'max_request_lock'):
        _lock_local.max_request_lock = asyncio.Semaphore(DEFAULT_CONCURRENT)
    return _lock_local.max_request_lock


headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'sec-ch-ua': '"Not_A Brand";v="99", "Microsoft Edge";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    # For baidu
    'Origin': 'https://fanyi.baidu.com',
    'Referer': 'https://fanyi.baidu.com/',
}

_sessions = weakref.WeakKeyDictionary()
atexit.register(lambda: [asyncio.run(s.close()) for s in _sessions.values()])


async def get_session():
    global _sessions

    loop = asyncio.get_running_loop()

    if loop in _sessions:
        return _sessions[loop]

    session = aiohttp.ClientSession(headers=headers)
    _sessions[loop] = session
    return session


def environment(fn):
    _cache = None
    _cache_time = None
    _cache_session = None

    def cache_need_refresh(refresh_time):
        nonlocal _cache_time
        if (
            not _cache
            or not _cache_time
            or (time.time() - _cache_time >= refresh_time)
        ):
            _cache_time = time.time()
            return True
        return False

    @functools.wraps(fn)
    async def wrapper(session):
        nonlocal _cache, _cache_session

        if cache_need_refresh(30) or session != _cache_session:
            _cache_session = session

            errors = None
            for _ in range(5):
                try:
                    _cache = data = await fn(session)
                    return data
                except Exception as err:
                    errors = err
            raise errors
        return _cache

    return wrapper


def run_sync(async_fn):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(async_fn)
