# opencc-py

[![CI](https://github.com/doggy8088/opencc-py/actions/workflows/ci.yml/badge.svg)](https://github.com/doggy8088/opencc-py/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/opencc-py-tw2.svg)](https://pypi.org/project/opencc-py-tw2/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

`opencc-py` 是依照 [Will 保哥的 C# OpenCC 實作](https://github.com/doggy8088/OpenCC)移植的純 Python OpenCC 函式庫。核心行為保留原實作的內嵌詞庫、locale/preset、Trie 最長匹配與多階段轉換流程。

## 範例

請參考 [`examples/`](examples/)，內含基本轉換、不套用詞彙轉換、不同簡繁詞庫差異、自訂詞典與 HTML/XML 轉換範例。

## 功能

- 純 Python 3.11+，無執行階段相依套件。
- 內建 `cn`、`hk`、`tw`、`tw2`、`twp`、`jp` locale。
- 支援 `full`、`cn2t`、`t2cn` preset。
- 支援自訂字典與多個字典群組串接。
- Unicode code point 層級的 Trie 最長匹配。
- XML 相容 HTML 轉換與還原。
- 提供 `opencc-py` CLI。

## 安裝

```bash
pip install opencc-py-tw2
```

## 基本用法

```python
from opencc_py import converter

convert = converter("cn", "tw2")
print(convert("汉语"))  # 漢語
print(convert.convert("默认用户界面支持数据库和网络请求。"))
```

## Locale 與 preset

預設 `opencc_py.converter(from_, to)` 使用 full preset：

| locale | 說明 |
| --- | --- |
| `cn` | 中國大陸簡體 |
| `hk` | 香港繁體異體字 |
| `tw` | 台灣繁體異體字 |
| `tw2` | 台灣繁體常用詞 |
| `twp` | 台灣繁體含 IT、姓名與其他詞彙 |
| `jp` | 日本新字體/異體字 |
| `t` | 直接通過，不載入該階段字典 |

方向限定 preset：

```python
from opencc_py import presets

cn_to_tw = presets.cn2t.converter("cn", "tw2")
tw_to_cn = presets.t2cn.converter("tw2", "cn")
```

## 自訂字典

字串格式與 C# 實作相同：每筆 `來源 目標`，筆與筆之間以 `|` 分隔；若詞條內含空白，可用 tab 分隔來源與目標。

```python
from opencc_py import DictEntry, custom_converter

convert = custom_converter("香蕉 banana|蘋果 apple|Web 平台庫\tWeb 平台函式庫")
print(convert("香蕉 蘋果 Web 平台庫"))

convert2 = custom_converter([
    DictEntry("“", "「"),
    DictEntry("”", "」"),
])
```

## 進階組合

`converter_factory()` 會依序套用每個 `DictGroup`，等同 C# 版本先處理 `from` 群組，再處理 `to` 群組。

```python
from opencc_py import DictEntry, DictGroup, converter_factory

first = DictGroup.from_entries([DictEntry("a", "b")])
second = DictGroup.from_entries([DictEntry("b", "c")])
convert = converter_factory(first, second)
print(convert("a"))  # c
```

## XML 相容 HTML 轉換

此功能使用 Python 標準函式庫 `xml.etree.ElementTree`，適用於可被 XML parser 解析的 HTML/XML。它會轉換符合 `lang` 範圍內的文字、`meta[name=description|keywords]` 的 `content`、`img alt`、`input[type=button] value`，並略過 `script`、`style` 與 `ignore-opencc` class。

```python
from opencc_py import HtmlConverter, converter

convert = converter("hk", "cn")
html = HtmlConverter.from_xml_string(
    convert,
    "<html lang='zh-HK'><body><p lang='zh-HK'>漢語</p></body></html>",
    "zh-HK",
    "zh-CN",
)
html.convert()
print(html.to_xml_string())
html.restore()
```

## CLI

```bash
opencc-py input.txt cn tw2
opencc-py input.txt cn tw2 -o output.txt
opencc-py input.txt cn tw2 --in-place
```

`-o/--output` 與 `-i/--in-place` 不能同時使用。輸入與輸出皆使用 UTF-8。

## 範例

更多可執行範例請見 [`samples/`](samples/)。

## 開發

```bash
python -m venv .venv
source .venv/bin/activate
python -m unittest discover -s tests
python -m pip install build
python -m build
```

如果 C# OpenCC 原始碼與本專案位於同一個父目錄，可重新產生內嵌詞庫：

```bash
python tools/generate_dict_data.py
python -m unittest discover -s tests
```

## 發布

PyPI 發布流程請見 [PUBLISHING.md](PUBLISHING.md)。

## 授權

MIT
