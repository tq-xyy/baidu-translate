import warnings
from typing import Union

from .api import langdetect, v2transapi
from .domain import Domain, check_domain
from .languages import Lang, lang_from_string
from .utils import run_sync, get_session

__all__ = ['translate_text', 'detect_language', 'Domain', 'Lang']

# We place the function here because it need call api to detect language.


def _normalize_language(detected, fromLang, toLang):
    if not isinstance(fromLang, Lang):
        fromLang = lang_from_string(fromLang)
    if not isinstance(toLang, Lang):
        toLang = lang_from_string(toLang)

    if fromLang == Lang.AUTO:
        fromLang = lang_from_string(detected)
    if toLang == Lang.AUTO:
        toLang = Lang.EN if fromLang == Lang.ZH else Lang.ZH

    return fromLang, toLang


async def translate_text_async(
    content: str, /,
    from_: Union[str, Lang] = Lang.AUTO, to: Union[str, Lang] = Lang.AUTO,
    domain: Domain = Domain.COMMON
) -> str:
    if not content:
        return content
    
    session = await get_session()
    
    detected = await langdetect(content, session=session)
    from_, to = _normalize_language(detected, from_, to)
    if from_ == to:
        return content

    if not check_domain(domain, from_, to):
        warnings.warn(
            f'Domain.{domain.name} don\'t match with fromLang {from_} and toLang {to}', stacklevel=2)
        domain = Domain.COMMON

    result = await v2transapi(content, from_.value, to.value, domain.value, session=session)

    if 'error' in result:
        raise Exception(result['errmsg'] + ' (%s)' % result['error'])

    dst = []
    for row in result['trans_result']['data']:
        dst.append(row['dst'])

    return '\n'.join(dst)


async def detect_language_async(content: str, /) -> Union[Lang, None]:
    if not content:
        return None
    try:
        session = await get_session()
        lang = await langdetect(content, session=session)
        if not lang:
            lang = None
    except:
        lang = None

    if lang:
        return lang_from_string(lang)
    return None


def translate_text(
    content: str, /,
    from_: Union[str, Lang] = Lang.AUTO, to: Union[str, Lang] = Lang.AUTO,
    domain: Domain = Domain.COMMON
) -> str:
    return run_sync(translate_text_async(content, from_, to, domain))


def detect_language(content: str) -> Union[Lang, None]:
    return run_sync(detect_language_async(content))
