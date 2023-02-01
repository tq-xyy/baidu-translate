# baidu-translate

一个免费, 高效, 简洁 [百度翻译](https://fanyi.baidu.com/) 接口

特点:

-   采用百度翻译公共接口, 无鉴权, 完全免费。
-   支持垂直翻译, 可提高翻译准确度。
-   代码内部自动获取 Token 和 GTK, 无需使用者手动获取。
-   接口简洁, 没有复杂的前置调用。
-   相对于同类开源项目而言, sign 算法采用 Python 重新编写, 无需额外的依赖和调用开销。
-   得益于缓存机制，首次调用可能稍慢，但后续调用相当之快。

## 安装

本项目仍处于快速开发状态，未发布到 PYPI，你可以通过以下方法来安装。

```sh
$ pip install git+https://github.com/17097239132/baidu-translate.git
```

## 例子

```python
import baidu_translate as fanyi

result = fanyi.translate_text('Hello, World!')
result_ru = fanyi.translate_text('Hello, World!', to=fanyi.Lang.RU)
print(result, result_ru)
# 你好，世界！ Здравствуйте, Мир!

lang = fanyi.detect_language('Vue rapide')
print(lang == fanyi.Lang.FRA)
# True

result = fanyi.translate_text('我们是中国人，我们爱自己的祖国！')
print(result)
# We are Chinese, we love our motherland!

result_common = fanyi.translate_text('年化收益率')
result_domain = fanyi.translate_text('年化收益率', domain=fanyi.Domain.FINANCE) # 金融
print(result_common, '&', result_domain)
# Annualized rate of return & Annualized yield
```

你也可以使用异步和多线程:

```python
import baidu_translate as fanyi
import asyncio, time
from concurrent.futures import ThreadPoolExecutor

# Make cache
fanyi.translate_text('Hi!')

langs = ['zh', 'en', 'fra', 'ru', 'ara', 'spa']


def test_sync(text):
    texts = []
    for lang in langs:
        texts.append(fanyi.translate_text(text, to=lang))

    return ' '.join(texts)


async def test_async(text):
    tasks = []
    for lang in langs:
        tasks.append(fanyi.translate_text_async(text, to=lang))
    texts = await asyncio.gather(*tasks)

    return ' '.join(texts)


def test_thread(text):
    with ThreadPoolExecutor() as pool:
        texts = pool.map(
            lambda lang: fanyi.translate_text(text, to=lang), langs
        )

    return ' '.join(texts)


start = time.time()
result_sync = test_sync('Good morning!')
print('Sync Time:', time.time() - start) # 1s~

start = time.time()
result_async = asyncio.run(test_async('Good morning!'))
print('Async Time:', time.time() - start) # 2s~

start = time.time()
result_thread = test_thread('Good morning!')
print('Thread Time:', time.time() - start) # 0.5s~

print(result_sync == result_async == result_thread)
# True
```

为了规避百度对并发的限制，异步模式将会加锁，所以通常情况下，多线程>同步>异步，但是在服务器环境下，异步模式可以有效地提高吞吐量，而多线程适合大规模翻译，同步则用于工具类项目。请根据使用场景自行抉择。

## API

### baidu_translate.translate_text(content, /, from_=Lang.AUTO, to=Lang.AUTO, domain=Domain.COMMON)

翻译 `content` 中的内容, 并返回一个字符串。

`from_` 和 `to` 分别是翻译的源语言和目标语言。接受一个 `Lang` 对象, 也可传入一个字符串, 将自动转化为 `Lang` 对象。如果未指定或为 `Lang.AUTO`, 将自动检测源语言或目标语言。

`domain` 是垂直翻译领域，请传入一个 `Domain` 对象。

如果 `content` 为空或源语言与目标语言相同将不做更改。

### baidu_translate.detect_language(content)

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

## 参考文献

1. [hujingshuang 的百度翻译 API](https://github.com/ZCY01/BaiduTranslate) ([百度翻译接口 破解](https://blog.csdn.net/hujingshuang/article/details/80180294))
2. [百度指数 Cipher-Text、百度翻译 Acs-Token 逆向分析](https://juejin.cn/post/7133151365806686245)
3. [js逆向-最新版百度翻译参数解密](https://blog.csdn.net/weixin_46672080/article/details/126533612)
4. [python的AES-CBC加密](https://zhuanlan.zhihu.com/p/184968023)

## 版权 & 免责声明

本项目已被放入*公有领域*，作者**放弃**所有权利。任何人都可以自由地使用本项目，而无需注明作者。

但值得注意的是，本项目违反了[百度翻译（PC 版）用户使用协议](https://fanyi.baidu.com/static/webpage/agreement.html)的第三十一条第一款。百度公司随时可以联系本人删除项目，但由此衍生出的任何法律问题本人概不负责（包括但不限于用户使用不当而对百度公司服务器造成的损失）。

特别提醒：本项目仅供**学习讨论**。建议不要在商业项目中使用，以规避法律风险。

且用且珍惜！
