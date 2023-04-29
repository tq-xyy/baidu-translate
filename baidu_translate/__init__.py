import warnings
from typing import Union

from httpx import AsyncClient

from .api import langdetect, transapi, v2transapi
from .domain import Domain, check_domain
from .errors import TranslateError, select_error
from .languages import Lang, lang_from_string, normalize_language
from .utils import get_session, run_sync, set_config

__all__ = [
    'translate_text',
    'detect_language',
    'Domain',
    'Lang',
    'TranslateError',
    'set_config',
]


async def translate_text_async(
    content: str,
    /,
    from_: Union[str, Lang] = Lang.AUTO,
    to: Union[str, Lang] = Lang.AUTO,
    domain: Domain = Domain.COMMON,
    *,
    session: AsyncClient = None,
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

    if domain == Domain.COMMON:
        result = await transapi(content, fromLang.value, toLang.value, session=session)
    else:
        result = await v2transapi(
            content,
            fromLang.value,
            toLang.value,
            domain.value,
            session=session,
        )

    errors = result.get_errors()
    if errors:
        code, msg = errors
        raise select_error(code)(f'{msg} (code {code})')

    return str(result)


async def detect_language_async(
    content: str, /, *, session: AsyncClient = None
) -> Union[Lang, None]:
    if not content:
        return None

    if not session:
        session = await get_session()

    lang = None
    try:
        lang = await langdetect(content, session=session)
    except Exception as e:
        raise e
        pass

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
    session: AsyncClient = None,
) -> str:
    return run_sync(translate_text_async(content, from_, to, domain, session=session))


def detect_language(
    content: str, /, *, session: AsyncClient = None
) -> Union[Lang, None]:
    return run_sync(detect_language_async(content, session=session))
