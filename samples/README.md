# opencc-py 範例

這個資料夾包含 `opencc-py-tw2` 的可執行範例。

## 安裝套件

```bash
python3 -m pip install opencc-py-tw2
```

或將目前工作目錄以可編輯模式安裝：

```bash
python3 -m pip install -e .
```

## 執行範例

```bash
python3 samples/basic_conversion.py
python3 samples/article_cn_to_tw2.py
python3 samples/presets.py
python3 samples/custom_dictionary.py
python3 samples/html_conversion.py
python3 samples/cli_usage.py
```

## 使用 uv 執行單一範例

```bash
uv run --with opencc-py-tw2 python samples/article_cn_to_tw2.py
```

`cli_usage.py` 示範如何使用已安裝的 `opencc-py` 命令，並會自動建立暫存輸入與輸出檔案。
