# 不套用詞彙轉換

這個範例示範如何只做簡繁字形轉換，不套用臺灣或香港詞彙。

## 重點

- `converter("cn", "t")` 會轉成 OpenCC 標準繁體。
- `converter("cn", "tw2")` 會再套用臺灣常用詞彙。
- 若你的內容已經有自己的詞彙規範，通常應該先使用 `t`。

## 執行

```bash
python examples/no-phrase-conversion/example.py
```
