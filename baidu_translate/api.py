import re
import time
from functools import lru_cache

import requests

from .domain import Domain
from .sign import sign

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}

session = requests.Session()
cookies = None


def _fetch_gtk_and_token(retries=5):
    global cookies
    try:
        # Step 1: Get gtk and cookie
        response1 = session.get('https://fanyi.baidu.com/', headers=headers)

        gtk = re.search(r'window.gtk = "(.+?)";', response1.text)[1]

        cookies = response1.cookies

        # Step 2: Use the cookie to request to get token
        response2 = session.get('https://fanyi.baidu.com/',
                                headers=headers, cookies=cookies)

        token = re.search(r"token: '(.+?)',", response2.text)[1]

        return {
            'gtk': gtk,
            'token': token
        }
    except Exception as err:
        if retries <= 0:
            raise err

        return _fetch_gtk_and_token(retries=retries - 1)


token_cache = None

# refresh time: one minute


def get_token():
    global token_cache
    if not token_cache or (time.time() - token_cache[0] >= 60):
        token = _fetch_gtk_and_token()
        token_cache = [time.time(), token]
        return token

    return token_cache[1]


@lru_cache(maxsize=256)
def langdectet(content: str) -> str:
    res = session.post('https://fanyi.baidu.com/langdetect',
                       data={'query': content}, headers=headers, cookies=cookies).json()

    if res['msg'] == 'success' and res['lan']:
        return res['lan']


@lru_cache(maxsize=256)
def v2transapi(content: str, fromLang: str, toLang: str, domain: Domain) -> dict:
    tokens = get_token()

    data = {
        'from': fromLang,
        'to': toLang,
        'query': content,
        'transtype': 'translang',
        'simple_means_flag': 3,
        'sign': sign(content, tokens['gtk']),
        'token': tokens['token'],
        'domain': domain.value,
    }

    res = session.post(
        'https://fanyi.baidu.com/v2transapi',
        headers=headers,
        params={'from': fromLang, 'to': toLang},
        data=data,
        cookies=cookies
    )
    return res.json()
