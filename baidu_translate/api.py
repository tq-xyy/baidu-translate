import re
import urllib.parse

from .domain import Domain
from .languages import Lang
from .sign import sign
from .utils import environment, headers, session

cookies = None


@environment
def _fetch_gtk_and_token():
    global cookies

    # Step 1: Get gtk and cookie
    response1 = session.get('https://fanyi.baidu.com/', headers=headers)

    gtk = re.search(r'window.gtk *= *"(.+?)";?', response1.text)[1]

    cookies = response1.cookies

    # Step 2: Use the cookie to request to get token
    response2 = session.get('https://fanyi.baidu.com/',
                            headers=headers, cookies=cookies)

    token = re.search(r"token: *'(.+?)',?", response2.text)[1]

    return gtk, token


def langdectet(content: str) -> str:
    result = session.post('https://fanyi.baidu.com/langdetect',
                          data={'query': content}, headers=headers, cookies=cookies).json()

    if result.get('msg', None) == 'success' and result.get('lan', None):
        return result['lan']


def v2transapi(content: str, fromLang: Lang, toLang: Lang, domain: Domain) -> dict:
    gtk, token = _fetch_gtk_and_token()

    data = {
        'from': fromLang.value,
        'to': toLang.value,
        'query': content,
        'transtype': 'translang',
        'simple_means_flag': 3,
        'sign': sign(content, gtk),
        'token': token,
        'domain': domain.value,
    }

    response = session.post(
        'https://fanyi.baidu.com/v2transapi',
        headers=headers,
        params={'from': fromLang, 'to': toLang},
        data=data,
        cookies=cookies
    )
    return response.json()
