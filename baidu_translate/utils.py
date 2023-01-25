import asyncio
import atexit
import functools
import time
import weakref

import aiohttp

# Due to Baidu's limitations, we cannot submit many requests at once.
max_request_lock = asyncio.Semaphore(1)

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    # For baidu
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
            not _cache or
            not _cache_time or
            (time.time() - _cache_time >= refresh_time)
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
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(async_fn)
