import enum
from .languages import Lang


class Domain(enum.Enum):
    COMMON = 'common'  # 通用领域
    BM = 'medicine'  # 生物医药
    ET = 'electronics'  # 电子科技
    WCM = 'mechanics'  # 水利机械
    NOVEL = 'novel'  # 网络文学
    FINANCE = 'finance'  # 金融
    MILITARY = 'military'  # 军事


def check_domain(domain: Domain, fromLang: Lang, toLang: Lang) -> bool:
    if domain == Domain.COMMON:
        return True

    if domain in (Domain.FINANCE, Domain.BM):
        chinese_english = (Lang.ZH, Lang.EN)
        return (fromLang in chinese_english) and (toLang in chinese_english)

    if domain in (Domain.NOVEL, Domain.ET, Domain.WCM):
        return fromLang == Lang.ZH and toLang == Lang.EN

    if domain == Domain.MILITARY:
        shouldFromLang = [
            Lang.EN,
            Lang.RU,
            Lang.JP,
            Lang.KOR,
            Lang.HI,
            Lang.FRA,
            Lang.DE,
            Lang.SPA,
            Lang.VIE,
        ]
        return fromLang in shouldFromLang and toLang == Lang.EN

    return False
