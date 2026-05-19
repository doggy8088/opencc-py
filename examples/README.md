# opencc-py 範例

這個資料夾收錄 `opencc-py` 的使用者範例。每個範例都是獨立資料夾，並附有 README 說明用途、執行方式與重點。

## 範例列表

| 範例 | 用途 |
| --- | --- |
| [basic-conversion](basic-conversion/) | 基本簡體轉臺灣繁體。 |
| [no-phrase-conversion](no-phrase-conversion/) | 只做字形轉換，不套用地區詞彙。 |
| [locale-differences](locale-differences/) | 比較不同簡繁詞庫輸出。 |
| [custom-dictionary](custom-dictionary/) | 使用自訂詞典與多階段轉換。 |
| [html-conversion](html-conversion/) | 轉換 XML/HTML 片段並還原。 |

## 執行方式

在 `opencc-py/` 目錄下，先安裝本機套件：

```bash
python -m pip install -e .
```

再執行範例：

```bash
python examples/basic-conversion/example.py
python examples/no-phrase-conversion/example.py
python examples/locale-differences/example.py
python examples/custom-dictionary/example.py
python examples/html-conversion/example.py
```
