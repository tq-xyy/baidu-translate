from .api import v2transapi, langdectet

def translate_text(content: str, /, from_='auto', to='auto') -> str:
    if from_ == 'auto':
        from_ = langdectet(content)
    if to == 'auto':
        to = 'en' if from_ == 'zh' else 'zh'
    result = v2transapi(content, from_, to)
    
    dst = []
    for row in result['trans_result']['data']:
        dst.append(row['dst'])
    
    return '\n'.join(dst)