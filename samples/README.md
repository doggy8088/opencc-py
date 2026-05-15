# opencc-py samples

This folder contains runnable examples for `opencc-py-tw2`.

## Install the package

```bash
python3 -m pip install opencc-py-tw2
```

Or install the current checkout in editable mode:

```bash
python3 -m pip install -e .
```

## Run the examples

```bash
python3 samples/basic_conversion.py
python3 samples/article_cn_to_tw2.py
python3 samples/presets.py
python3 samples/custom_dictionary.py
python3 samples/html_conversion.py
python3 samples/cli_usage.py
```

## Run one example with uv

```bash
uv run --with-requirements samples/requirements.txt python samples/article_cn_to_tw2.py
```

`cli_usage.py` demonstrates the installed `opencc-py` command and creates temporary input/output files automatically.
