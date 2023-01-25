import re

import aiohttp

from .sign import sign
from .utils import environment, max_request_lock


@environment
async def _fetch_gtk_and_token(session: aiohttp.ClientSession):
    # Step 1: Get gtk and cookie
    response1 = await session.get('https://fanyi.baidu.com/')
    gtk = re.search(r'window.gtk *= *"(.+?)";?', await response1.text())[1]

    # Step 2: Use the cookie to request to get token
    response2 = await session.get('https://fanyi.baidu.com/')
    token = re.search(r"token: *'(.+?)',?", await response2.text())[1]

    return gtk, token


async def langdetect(content: str, session: aiohttp.ClientSession) -> str:
    async with max_request_lock:
        resp = await session.post('https://fanyi.baidu.com/langdetect',
                                data={'query': content})
        result = await resp.json()

        if result.get('msg', None) == 'success' and result.get('lan', None):
            return result['lan']


async def v2transapi(content: str, fromLang: str, toLang: str, domain: str, session: aiohttp.ClientSession) -> dict:
    async with max_request_lock:
        gtk, token = await _fetch_gtk_and_token(session)

        data = {
            'from': fromLang,
            'to': toLang,
            'query': content,
            'transtype': 'translang',
            'simple_means_flag': 3,
            'sign': sign(content, gtk),
            'token': token,
            'domain': domain,
        }

        # you can ignore this, not required. But params can takes parts in data.
        params = {
            'from': fromLang,
            'to': toLang,
        }

        response = await session.post(
            'https://fanyi.baidu.com/v2transapi',
            params=params,
            data=data,
        )

        return await response.json()
