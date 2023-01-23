import warnings
from typing import Union

from .api import langdetect, v2transapi
from .domain import Domain, check_domain
from .languages import Lang, lang_from_string

__all__ = ['translate_text', 'detect_language', 'Domain', 'Lang']

# We place the function here because it need call api to detect language.


def _normalize_language(content, fromLang, toLang):
    if not isinstance(fromLang, Lang):
        fromLang = lang_from_string(fromLang)
    if not isinstance(toLang, Lang):
        toLang = lang_from_string(toLang)

    if fromLang == Lang.AUTO:
        fromLang = lang_from_string(langdetect(content))
    if toLang == Lang.AUTO:
        toLang = Lang.EN if fromLang == Lang.ZH else Lang.ZH

    return fromLang, toLang


def translate_text(
    content: str, /,
    from_: Union[str, Lang] = Lang.AUTO, to: Union[str, Lang] = Lang.AUTO,
    domain: Domain = Domain.COMMON
) -> str:
    if not content:
        return content

    from_, to = _normalize_language(content, from_, to)
    if from_ == to:
        return content

    if not check_domain(domain, from_, to):
        warnings.warn(
            f'Domain.{domain.name} don\'t match with fromLang {from_} and toLang {to}', stacklevel=2)
        domain = Domain.COMMON

    result = v2transapi(content, from_, to, domain)

    if 'error' in result:
        raise Exception(result['errmsg'])

    dst = []
    for row in result['trans_result']['data']:
        dst.append(row['dst'])

    return '\n'.join(dst)


def detect_language(content: str) -> Union[Lang, None]:
    if not content:
        return None
    try:
        lang = langdetect(content)
        if not lang:
            lang = None
    except:
        lang = None

    if lang:
        return lang_from_string(lang)
    return None
