import re
from urllib.parse import quote_plus

from aiohttp import ClientSession

from .sign import acs_token, sign
from .utils import environment, max_request_lock


@environment
async def _fetch_gtk_and_token(session: ClientSession):
    # Step 1: Get gtk and cookie
    response1 = await session.get('https://fanyi.baidu.com/')
    gtk = re.search(r'window.gtk *= *"(.+?)";?', await response1.text())[1]

    # Step 2: Use the cookie to request to get token
    response2 = await session.get('https://fanyi.baidu.com/')
    token = re.search(r"token: *'(.+?)',?", await response2.text())[1]

    return gtk, token


@environment
async def _fetch_acs_sign_js(session: ClientSession):
    resp = await session.get(
        'https://dlswbr.baidu.com/heicha/mm/2060/acs-2060.js'
    )
    return await resp.text(), resp.request_info.headers['User-Agent']


async def langdetect(content: str, session: ClientSession) -> str:
    async with max_request_lock():
        resp = await session.post(
            'https://fanyi.baidu.com/langdetect', data={'query': content}
        )
        result = await resp.json()

        if result.get('msg', None) == 'success' and result.get('lan', None):
            return result['lan']


async def v2transapi(
    content: str,
    fromLang: str,
    toLang: str,
    domain: str,
    session: ClientSession,
) -> dict:
    async with max_request_lock():
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

        acs_sign_js, user_agent = await _fetch_acs_sign_js(session)
        page = f'https://fanyi.baidu.com/#{fromLang}/{toLang}/{quote_plus(content)}'
        headers = {
            'Acs-Token': acs_token(acs_sign_js, page, user_agent),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

        response = await session.post(
            'https://fanyi.baidu.com/v2transapi',
            params=params,
            data=data,
            headers=headers,
        )

        return await response.json()
