# baidu-translate
一个免费, 高效, 简洁 [百度翻译](https://fanyi.baidu.com/) 接口

特点:
* 采用百度翻译公共接口, 无鉴权, 完全免费。
* 代码内部自动获取 Token 和 GTK, 无需使用者手动获取。
* 接口简洁, 没有复杂的前置调用。
* 相对于同类开源项目而言, sign 算法采用 Python 重新编写, 无需额外的依赖和调用开销。
* 得益于缓存机制，首次调用可能稍慢，但后续调用相当之快。

## API

翻译 API 接口请参见 [api.py](https://github.com/17097231932/baidu-translate/blob/main/baidu_translate/api.py), 源代码简洁易懂欢迎阅读。

```python

def translate_text(content: str, /, from_: str ='auto', to: str ='auto') -> str:...

# --- 原始接口 ---

# 检测语种
def langdectet(content: str) -> str:...

# 翻译 (注意此处返回的是原始数据, 没有文档, 请自行解析)
def v2transapi(content: str, fromLang: str, toLang: str) -> dict:...
```

## 参考

1. [hujingshuang 的百度翻译 API](https://github.com/ZCY01/BaiduTranslate) ([百度翻译接口 破解](https://blog.csdn.net/hujingshuang/article/details/80180294))

## 版权 & 免责声明

本项目已被放入公有领域，作者放弃所有权利。任何人都可以自由地使用本项目，而无需注明作者。

但值得注意的是，本项目违反了[百度翻译（PC版）用户使用协议](https://fanyi.baidu.com/static/webpage/agreement.html)的第三十一条第一款。百度公司随时可以联系本人删除项目，但由此衍生出的任何法律问题本人概不负责（包括但不限于用户使用不当而对百度公司服务器造成的损失）。

且用且珍惜！
