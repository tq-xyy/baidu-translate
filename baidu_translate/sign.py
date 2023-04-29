import base64
import json
import math
import time
from ast import PyCF_ONLY_AST

from Crypto.Cipher import AES

from .errors import NeedUpdate


def sign(string: str, gtk: str) -> str:
    if len(string) > 30:
        center = math.floor(len(string) / 2)
        string = string[:10] + string[center - 5 : center + 5] + string[-10:]

    [p, q] = map(int, gtk.split('.'))

    g = p

    for b in bytes(string, 'utf-8'):
        g += b
        g = (g + (g << 10)) & 0xFFFFFFFF
        g = g ^ (g >> 6)  # TODO: g = g ^ (g >>> 6)

    g = (g + (g << 3)) & 0xFFFFFFFF
    g = g ^ (g >> 11)  # TODO: g = g ^ (g >>> 6)
    g = ((g + (g << 15)) & 0xFFFFFFFF) ^ q

    if g <= 0:
        g = (0x7FFFFFFF & g) + 0x80000000

    g = g % 1000000

    return str(g) + '.' + str(g ^ p)


def acs_token(acs_sign_js: str, url: str, ua: str) -> str:
    def parsestr(str) -> str:
        return compile(f'"{str}"', '<hex>', 'eval', PyCF_ONLY_AST).body.value

    def pkcs7padding(text: bytes) -> bytes:
        padding = 16 - len(text) % 16
        padding_text = bytes([padding]) * padding
        return text + padding_text

    try:
        # Absolute Locate
        if acs_sign_js[16708] == ',' and acs_sign_js[16722] == ']':
            arg0 = parsestr(acs_sign_js[16709:16722])

        if acs_sign_js[16853] == "'" and acs_sign_js[16918] == "'":
            arg1 = parsestr(acs_sign_js[16854:16918])

        if acs_sign_js[16920] == "'" and acs_sign_js[16985] == "'":
            arg2 = parsestr(acs_sign_js[16921:16985])

        assert len(arg0) == 13
        assert len(arg1) == 16
        assert len(arg2) == 16
    except (
        AssertionError,
        NameError,
        AttributeError,
        SyntaxError,
        IndexError,
    ) as err:
        bug_report = 'https://github.com/17097231932/baidu-translate/issues/new/choose'
        raise NeedUpdate(
            'Can\'t get the secret key. '
            f'It is possible that Baidu has updated. To report bugs, please visit {bug_report}.'
        ) from err
    ts = math.floor(time.time() * 1000)

    data = json.dumps(
        {
            0: "145672893382649882066085",
            'ua': ua,
            'platform': 'Win32',
            'd1': '',
            'd2': 0,
            'clientTs': ts,
            'odkp': 1,
            'version': '1.1.0.3',
        },
        separators=(',', ':'),
    )

    cipher = AES.new(arg1.encode('latin-1'), AES.MODE_CBC, arg2.encode('latin-1'))
    data = cipher.encrypt(pkcs7padding(data.encode('utf-8')))
    return arg0 + '_' + str(ts) + '_' + base64.b64encode(data).decode('utf-8')
