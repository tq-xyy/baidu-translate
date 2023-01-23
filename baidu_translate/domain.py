import enum


class Domain(enum.Enum):
    COMMON = 'common'      # 通用领域
    BM = 'medicine'        # 生物医药
    ET = 'electronics'     # 电子科技
    WCM = 'mechanics'      # 水利机械
    NOVEL = 'novel'        # 网络文学
    FINANCE = 'finance'    # 金融
    MILITARY = 'military'  # 军事


def check_domain(domain: Domain, fromLang: str, toLang: str):
    chinese_english = ('zh', 'en')

    if domain == Domain.COMMON:
        return True
    if domain in (Domain.FINANCE, Domain.BM):
        return (fromLang in chinese_english) and (toLang in chinese_english)
    if domain in (Domain.NOVEL, Domain.ET, Domain.WCM):
        return fromLang == 'zh' and toLang == 'en'
    if domain == Domain.MILITARY:
        shouldFromLang = ['en', 'ru', 'jp', 'kor',
                          'hi', 'fra', 'de', 'spa', 'vie']
        return fromLang in shouldFromLang and toLang == 'en'
    return False
