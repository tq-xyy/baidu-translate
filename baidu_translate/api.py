import re

# from urllib.parse import quote_plus

from httpx import AsyncClient

from .models import (
    TransapiSentenceResult,
    TransapiWordResult,
    V2TransapiResult,
)
from .sign import acs_token, sign
from .utils import be_losse_cookies, environment, max_request_lock


@environment
async def _fetch_cookie(session: AsyncClient):
    if len(session.cookies.values()) > 0:
        return

    if not be_losse_cookies():
        await session.get('https://www.baidu.com/')
        await session.get('https://hector.baidu.com/a.js')

    await session.get('https://fanyi.baidu.com/')

    session.cookies.update(
        {
            'APPGUIDE_10_0_2': '1',
            'REALTIME_TRANS_SWITCH': '1',
            'FANYI_WORD_SWITCH': '1',
            'HISTORY_SWITCH': '1',
            'SOUND_SPD_SWITCH': '1',
            'SOUND_PREFER_SWITCH': '1',
        }
    )


@environment
async def _fetch_gtk_and_token(session: AsyncClient):
    response = await session.get('https://fanyi.baidu.com/')
    gtk = re.search(r'window.gtk *= *"(.+?)";?', response.text)[1]
    token = re.search(r"token: *'(.+?)',?", response.text)[1]

    return gtk, token


@environment
async def _fetch_acs_sign_js(session: AsyncClient):
    resp = await session.get('https://dlswbr.baidu.com/heicha/mm/2060/acs-2060.js')
    return resp.text, resp.request.headers['User-Agent']


async def langdetect(content: str, session: AsyncClient) -> str:
    await _fetch_cookie(session)

    async with max_request_lock():
        resp = await session.post(
            'https://fanyi.baidu.com/langdetect', data={'query': content}
        )
        result = resp.json()

        if result.get('msg', None) == 'success' and result.get('lan', None):
            return result['lan']


async def v2transapi(
    content: str,
    fromLang: str,
    toLang: str,
    domain: str,
    session: AsyncClient,
):
    await _fetch_cookie(session)

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

        # acs_sign_js, user_agent = await _fetch_acs_sign_js(session)
        # page = f'https://fanyi.baidu.com/#{fromLang}/{toLang}/{quote_plus(content)}'
        headers = {
            # 'Acs-Token': acs_token(acs_sign_js, page, user_agent),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

        response = await session.post(
            'https://fanyi.baidu.com/v2transapi',
            params=params,
            data=data,
            headers=headers,
        )

        return V2TransapiResult(response.json())


async def transapi(content: str, fromLang: str, toLang: str, session: AsyncClient):
    await _fetch_cookie(session)

    data = {
        'from': fromLang,
        'to': toLang,
        'query': content,
        'source': 'txt',
    }

    async with max_request_lock():
        resp = await session.post('https://fanyi.baidu.com/transapi', data=data)
        result = resp.json()

        if result.get('type', None) == 1:
            return TransapiWordResult(result)
        else:
            return TransapiSentenceResult(result)
