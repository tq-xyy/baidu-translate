import enum
from typing import Tuple, Union

from .errors import UnknownLanguage


class Lang(enum.Enum):
    # will be replace with real language
    AUTO = 'auto'  # 自动检测

    # Common Languages
    ZH = 'zh'  # 中文(简体)
    EN = 'en'  # 英语
    SPA = 'spa'  # 西班牙语
    ARA = 'ara'  # 阿拉伯语
    FRA = 'fra'  # 法语
    RU = 'ru'  # 俄语

    # More Languages
    JP = 'jp'  # 日语
    TH = 'th'  # 泰语
    KOR = 'kor'  # 韩语
    DE = 'de'  # 德语
    PT = 'pt'  # 葡萄牙语
    IT = 'it'  # 意大利语
    EL = 'el'  # 希腊语
    NL = 'nl'  # 荷兰语
    PL = 'pl'  # 波兰语
    FIN = 'fin'  # 芬兰语
    CS = 'cs'  # 捷克语
    BUL = 'bul'  # 保加利亚语
    DAN = 'dan'  # 丹麦语
    EST = 'est'  # 爱沙尼亚语
    HU = 'hu'  # 匈牙利语
    ROM = 'rom'  # 罗马尼亚语
    SLO = 'slo'  # 斯洛文尼亚语
    SWE = 'swe'  # 瑞典语
    VIE = 'vie'  # 越南语
    YUE = 'yue'  # 中文(粤语)
    CHT = 'cht'  # 中文(繁体)
    WYW = 'wyw'  # 中文(文言文)
    AFR = 'afr'  # 南非荷兰语
    ALB = 'alb'  # 阿尔巴尼亚语
    AMH = 'amh'  # 阿姆哈拉语
    ARM = 'arm'  # 亚美尼亚语
    ASM = 'asm'  # 阿萨姆语
    AST = 'ast'  # 阿斯图里亚斯语
    AZE = 'aze'  # 阿塞拜疆语
    BAQ = 'baq'  # 巴斯克语
    BEL = 'bel'  # 白俄罗斯语
    BEN = 'ben'  # 孟加拉语
    BOS = 'bos'  # 波斯尼亚语
    BUR = 'bur'  # 缅甸语
    CAT = 'cat'  # 加泰罗尼亚语
    CEB = 'ceb'  # 宿务语
    HRV = 'hrv'  # 克罗地亚语
    EPO = 'epo'  # 世界语
    FAO = 'fao'  # 法罗语
    FIL = 'fil'  # 菲律宾语
    GLG = 'glg'  # 加利西亚语
    GEO = 'geo'  # 格鲁吉亚语
    GUJ = 'guj'  # 古吉拉特语
    HAU = 'hau'  # 豪萨语
    HEB = 'heb'  # 希伯来语
    HI = 'hi'  # 印地语
    ICE = 'ice'  # 冰岛语
    IBO = 'ibo'  # 伊博语
    ID = 'id'  # 印尼语
    GLE = 'gle'  # 爱尔兰语
    KAN = 'kan'  # 卡纳达语
    KLI = 'kli'  # 克林贡语
    KUR = 'kur'  # 库尔德语
    LAO = 'lao'  # 老挝语
    LAT = 'lat'  # 拉丁语
    LAV = 'lav'  # 拉脱维亚语
    LIT = 'lit'  # 立陶宛语
    LTZ = 'ltz'  # 卢森堡语
    MAC = 'mac'  # 马其顿语
    MG = 'mg'  # 马拉加斯语
    MAY = 'may'  # 马来语
    MAL = 'mal'  # 马拉雅拉姆语
    MLT = 'mlt'  # 马耳他语
    MAR = 'mar'  # 马拉地语
    NEP = 'nep'  # 尼泊尔语
    NNO = 'nno'  # 新挪威语
    PER = 'per'  # 波斯语
    SRD = 'srd'  # 萨丁尼亚语
    SRP = 'srp'  # 塞尔维亚语(拉丁文)
    SIN = 'sin'  # 僧伽罗语
    SK = 'sk'  # 斯洛伐克语
    SOM = 'som'  # 索马里语
    SWA = 'swa'  # 斯瓦希里语
    TGL = 'tgl'  # 他加禄语
    TGK = 'tgk'  # 塔吉克语
    TAM = 'tam'  # 泰米尔语
    TAT = 'tat'  # 鞑靼语
    TEL = 'tel'  # 泰卢固语
    TR = 'tr'  # 土耳其语
    TUK = 'tuk'  # 土库曼语
    UKR = 'ukr'  # 乌克兰语
    URD = 'urd'  # 乌尔都语
    OCI = 'oci'  # 奥克语
    KIR = 'kir'  # 吉尔吉斯语
    PUS = 'pus'  # 普什图语
    HKM = 'hkm'  # 高棉语
    HT = 'ht'  # 海地语
    NOB = 'nob'  # 书面挪威语
    PAN = 'pan'  # 旁遮普语
    ARQ = 'arq'  # 阿尔及利亚阿拉伯语
    BIS = 'bis'  # 比斯拉马语
    FRN = 'frn'  # 加拿大法语
    HAK = 'hak'  # 哈卡钦语
    HUP = 'hup'  # 胡帕语
    ING = 'ing'  # 印古什语
    LAG = 'lag'  # 拉特加莱语
    MAU = 'mau'  # 毛里求斯克里奥尔语
    MOT = 'mot'  # 黑山语
    POT = 'pot'  # 巴西葡萄牙语
    RUY = 'ruy'  # 卢森尼亚语
    SEC = 'sec'  # 塞尔维亚-克罗地亚语
    SIL = 'sil'  # 西里西亚语
    TUA = 'tua'  # 突尼斯阿拉伯语
    ACH = 'ach'  # 亚齐语
    AKA = 'aka'  # 阿肯语
    ARG = 'arg'  # 阿拉贡语
    AYM = 'aym'  # 艾马拉语
    BAL = 'bal'  # 俾路支语
    BAK = 'bak'  # 巴什基尔语
    BEM = 'bem'  # 本巴语
    BER = 'ber'  # 柏柏尔语
    BHO = 'bho'  # 博杰普尔语
    BLI = 'bli'  # 比林语
    BRE = 'bre'  # 布列塔尼语
    CHR = 'chr'  # 切罗基语
    NYA = 'nya'  # 齐切瓦语
    CHV = 'chv'  # 楚瓦什语
    COR = 'cor'  # 康瓦尔语
    COS = 'cos'  # 科西嘉语
    CRE = 'cre'  # 克里克语
    CRI = 'cri'  # 克里米亚鞑靼语
    DIV = 'div'  # 迪维希语
    ENO = 'eno'  # 古英语
    FRM = 'frm'  # 中古法语
    FRI = 'fri'  # 弗留利语
    FUL = 'ful'  # 富拉尼语
    GLA = 'gla'  # 盖尔语
    LUG = 'lug'  # 卢干达语
    GRA = 'gra'  # 古希腊语
    GRN = 'grn'  # 瓜拉尼语
    HAW = 'haw'  # 夏威夷语
    HIL = 'hil'  # 希利盖农语
    IDO = 'ido'  # 伊多语
    INA = 'ina'  # 因特语
    IKU = 'iku'  # 伊努克提图特语
    JAV = 'jav'  # 爪哇语
    KAB = 'kab'  # 卡拜尔语
    KAL = 'kal'  # 格陵兰语
    KAU = 'kau'  # 卡努里语
    KAS = 'kas'  # 克什米尔语
    KAH = 'kah'  # 卡舒比语
    KIN = 'kin'  # 卢旺达语
    KON = 'kon'  # 刚果语
    KOK = 'kok'  # 孔卡尼语
    LIM = 'lim'  # 林堡语
    LIN = 'lin'  # 林加拉语
    LOJ = 'loj'  # 逻辑语
    LOG = 'log'  # 低地德语
    LOS = 'los'  # 下索布语
    MAI = 'mai'  # 迈蒂利语
    GLV = 'glv'  # 曼克斯语
    MAO = 'mao'  # 毛利语
    MAH = 'mah'  # 马绍尔语
    NBL = 'nbl'  # 南恩德贝莱语
    NEA = 'nea'  # 那不勒斯语
    NQO = 'nqo'  # 西非书面语
    SME = 'sme'  # 北方萨米语
    NOR = 'nor'  # 挪威语
    OJI = 'oji'  # 奥杰布瓦语
    ORI = 'ori'  # 奥里亚语
    ORM = 'orm'  # 奥罗莫语
    OSS = 'oss'  # 奥塞梯语
    PAM = 'pam'  # 邦板牙语
    PAP = 'pap'  # 帕皮阿门托语
    PED = 'ped'  # 北索托语
    QUE = 'que'  # 克丘亚语
    ROH = 'roh'  # 罗曼什语
    RO = 'ro'  # 罗姆语
    SM = 'sm'  # 萨摩亚语
    SAN = 'san'  # 梵语
    SCO = 'sco'  # 苏格兰语
    SHA = 'sha'  # 掸语
    SNA = 'sna'  # 修纳语
    SND = 'snd'  # 信德语
    SOL = 'sol'  # 桑海语
    SOT = 'sot'  # 南索托语
    SYR = 'syr'  # 叙利亚语
    TET = 'tet'  # 德顿语
    TIR = 'tir'  # 提格利尼亚语
    TSO = 'tso'  # 聪加语
    TWI = 'twi'  # 契维语
    UPS = 'ups'  # 高地索布语
    VEN = 'ven'  # 文达语
    WLN = 'wln'  # 瓦隆语
    WEL = 'wel'  # 威尔士语
    FRY = 'fry'  # 西弗里斯语
    WOL = 'wol'  # 沃洛夫语
    XHO = 'xho'  # 科萨语
    YID = 'yid'  # 意第绪语
    YOR = 'yor'  # 约鲁巴语
    ZAZ = 'zaz'  # 扎扎其语
    ZUL = 'zul'  # 祖鲁语
    SUN = 'sun'  # 巽他语
    HMN = 'hmn'  # 苗语
    SRC = 'src'  # 塞尔维亚语(西里尔文)


def lang_from_string(string: Union[str, Lang]) -> Lang:
    if isinstance(string, Lang):
        return string

    if string not in Lang._value2member_map_:
        raise UnknownLanguage('Unsupported language ' + string)
    return Lang._value2member_map_[string]


def normalize_language(
    detected: str, fromLang: Union[Lang, str], toLang: Union[Lang, str]
) -> Tuple[Lang, Lang]:
    fromLang = lang_from_string(fromLang)
    toLang = lang_from_string(toLang)

    if fromLang == Lang.AUTO:
        if not detected:
            raise UnknownLanguage(
                'Can\'t detect language, please set `from_` argument.'
            )
        fromLang = lang_from_string(detected)
    if toLang == Lang.AUTO:
        toLang = Lang.EN if fromLang == Lang.ZH else Lang.ZH

    return fromLang, toLang
