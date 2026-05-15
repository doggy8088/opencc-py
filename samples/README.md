# opencc-py samples

This folder contains runnable examples for `opencc-py-tw2`.

## Run from the repository

```bash
PYTHONPATH=src python3 samples/basic_conversion.py
PYTHONPATH=src python3 samples/article_cn_to_tw2.py
PYTHONPATH=src python3 samples/presets.py
PYTHONPATH=src python3 samples/custom_dictionary.py
PYTHONPATH=src python3 samples/html_conversion.py
PYTHONPATH=src python3 samples/cli_usage.py
```

## Run with uv outside the repository

```bash
uv run --with-requirements samples/requirements.txt python samples/article_cn_to_tw2.py
```

`cli_usage.py` demonstrates the installed `opencc-py` command and creates temporary input/output files automatically.
