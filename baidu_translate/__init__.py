from .api import v2transapi, langdectet
from .domain import Domain, check_domain
import warnings

__all__ = ['translate_text']


def translate_text(content: str, /, from_='auto', to='auto', domain: Domain = Domain.COMMON) -> str:
    if from_ == 'auto':
        from_ = langdectet(content)
    if to == 'auto':
        to = 'en' if from_ == 'zh' else 'zh'
    if from_ == to:
        return content

    if not check_domain(domain, from_, to):
        warnings.warn(
            f'Domain.{domain.name} don\'t match with fromLang {from_} and toLang {to}', stacklevel=2)
        domain = Domain.COMMON

    result = v2transapi(content, from_, to, domain)

    dst = []
    for row in result['trans_result']['data']:
        dst.append(row['dst'])

    return '\n'.join(dst)
