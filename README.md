# baidu-translate

一个免费, 高效, 简洁 [百度翻译](https://fanyi.baidu.com/) 接口

特点:

-   采用百度翻译公共接口, 无鉴权, 完全免费。
-   支持垂直翻译, 可提高翻译准确度。
-   代码内部自动获取 Token 和 GTK, 无需使用者手动获取。
-   接口简洁, 没有复杂的前置调用。
-   相对于同类开源项目而言, sign 算法采用 Python 重新编写, 无需额外的依赖和调用开销。
-   得益于缓存机制，首次调用可能稍慢，但后续调用相当之快。

## Demo

```python
import baidu_translate as fanyi

result = fanyi.translate_text('Hello, World!')
result_ru = fanyi.translate_text('Hello, World!', to=fanyi.Lang.RU)
print(result, result_ru)
# 你好，世界！ Здравствуйте, Мир!

lang = fanyi.detcet_language('Vue rapide')
print(lang == fanyi.Lang.FRA)
# True

result = fanyi.translate_text('我们是中国人，我们爱自己的祖国！')
print(result)
# We are Chinese, we love our motherland!

result_common = fanyi.translate_text('年化收益率')
result_domain = fanyi.translate_text('年化收益率', domain=fanyi.Domain.FINANCE) # 金融
print(result_common, result_domain)
# Annualized rate of return & Annualized yield
```

## API

### baidu_translate.translate_text(content, /, from_=Lang.AUTO, to=Lang.AUTO, domain=Domain.COMMON)

翻译 `content` 中的内容, 并返回一个字符串。

`from_` 和 `to` 分别是翻译的源语言和目标语言。接受一个 `Lang` 对象, 也可传入一个字符串, 将自动转化为 `Lang` 对象。如果未指定或为 `Lang.AUTO`, 将自动检测源语言或目标语言。

`domain` 是垂直翻译领域，请传入一个 `Domain` 对象。

如果 `content` 为空或源语言与目标语言相同将不做更改。

### baidu_translate.detcet_language(content)

检测 `content` 的语种。返回一个 `Lang` 对象。如果检测不出来将返回 `None`。

### baidu_translate.Lang

枚举对象, 包含百度支持的所有语种的 ID, 请注意是全部大写。

*建议结合 IDE 自动补全使用。*

```python

class Lang(enum.Enum):
    # will be replace with real language
    AUTO = 'auto'  # 自动检测

    # Common Languages
    ZH = 'zh'    # 中文(简体)
    EN = 'en'    # 英语
    SPA = 'spa'  # 西班牙语
    ARA = 'ara'  # 阿拉伯语
    FRA = 'fra'  # 法语
    RU = 'ru'    # 俄语

    # More Languages
    ...
```

### baidu_translate.Domain

枚举对象, 百度的垂直翻译领域, 请注意是全部大写。

*建议结合 IDE 自动补全使用。*

```python
class Domain(enum.Enum):
    COMMON = 'common'      # 通用领域
    BM = 'medicine'        # 生物医药
    ET = 'electronics'     # 电子科技
    WCM = 'mechanics'      # 水利机械
    NOVEL = 'novel'        # 网络文学
    FINANCE = 'finance'    # 金融
    MILITARY = 'military'  # 军事
```

## 参考

1. [hujingshuang 的百度翻译 API](https://github.com/ZCY01/BaiduTranslate) ([百度翻译接口 破解](https://blog.csdn.net/hujingshuang/article/details/80180294))

## 版权 & 免责声明

本项目已被放入公有领域，作者放弃所有权利。任何人都可以自由地使用本项目，而无需注明作者。

但值得注意的是，本项目违反了[百度翻译（PC 版）用户使用协议](https://fanyi.baidu.com/static/webpage/agreement.html)的第三十一条第一款。百度公司随时可以联系本人删除项目，但由此衍生出的任何法律问题本人概不负责（包括但不限于用户使用不当而对百度公司服务器造成的损失）。

且用且珍惜！
