import warnings
from typing import Union

from aiohttp import ClientSession

from .api import langdetect, v2transapi
from .domain import Domain, check_domain
from .errors import TranslateError, select_error
from .languages import Lang, lang_from_string, normalize_language
from .utils import get_session, run_sync

__all__ = [
    'translate_text',
    'detect_language',
    'Domain',
    'Lang',
    'TranslateError',
]


async def translate_text_async(
    content: str,
    /,
    from_: Union[str, Lang] = Lang.AUTO,
    to: Union[str, Lang] = Lang.AUTO,
    domain: Domain = Domain.COMMON,
    *,
    session: ClientSession = None,
) -> str:
    if not content:
        return content

    if not session:
        session = await get_session()

    detected = await detect_language_async(content, session=session)
    fromLang, toLang = normalize_language(detected, from_, to)

    if fromLang == toLang:
        return content

    if not check_domain(domain, fromLang, toLang):
        warnings.warn(
            f'Domain.{domain.name} don\'t match with fromLang {fromLang} and toLang {toLang}',
            stacklevel=2,
        )
        domain = Domain.COMMON

    result = await v2transapi(
        content, fromLang.value, toLang.value, domain.value, session=session
    )

    if 'error' in result:
        msg = f"{result['errmsg']} (code {result['error']})"
        raise select_error(result['error'])(msg)

    dst = []
    for row in result['trans_result']['data']:
        dst.append(row['dst'])

    return '\n'.join(dst)


async def detect_language_async(
    content: str, /, *, session: ClientSession = None
) -> Union[Lang, None]:
    if not content:
        return None

    if not session:
        session = await get_session()

    try:
        lang = await langdetect(content, session=session)
        if not lang:
            lang = None
    except:
        lang = None

    if lang:
        return lang_from_string(lang)
    return None


def translate_text(
    content: str,
    /,
    from_: Union[str, Lang] = Lang.AUTO,
    to: Union[str, Lang] = Lang.AUTO,
    domain: Domain = Domain.COMMON,
    *,
    session: ClientSession = None,
) -> str:
    return run_sync(
        translate_text_async(content, from_, to, domain, session=session)
    )


def detect_language(
    content: str, /, *, session: ClientSession = None
) -> Union[Lang, None]:
    return run_sync(detect_language_async(content, session=session))
