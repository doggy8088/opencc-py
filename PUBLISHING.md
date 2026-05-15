# PyPI 發布指南

這份文件說明如何把本專案順利發布到 PyPI。

本專案的名稱設定如下：

| 項目 | 值 |
| --- | --- |
| GitHub 儲存庫 | `doggy8088/opencc-py` |
| PyPI 發布套件 | `opencc-py-tw2` |
| Python import 套件 | `opencc_py` |
| CLI 命令 | `opencc-py` |
| 發布 workflow | `.github/workflows/publish.yml` |
| GitHub environment 環境 | `pypi` |

> `opencc-py` 這個 PyPI 發布名稱已被既有專案使用，所以本專案發布名稱是 `opencc-py-tw2`。

## 1. 發布前檢查

先確認 main branch 是乾淨狀態，且版本號正確。

```bash
git status --short
grep '^version = ' pyproject.toml
```

確認 `pyproject.toml` 內的版本，例如：

```toml
version = "0.1.0"
```

GitHub Release tag 應使用相同版本並加上 `v` 前綴，例如 `v0.1.0`。

## 2. 本機驗證

建議使用 venv，避免 macOS/Homebrew Python 的 PEP 668 限制。

```bash
python3 -m venv .venv-release
source .venv-release/bin/activate
python -m pip install --upgrade pip build twine

PYTHONPATH=src python -m unittest discover -s tests
python -m build
twine check dist/*
```

再從本機 wheel 安裝一次做 smoke test：

```bash
python -m venv .venv-smoke
source .venv-smoke/bin/activate
python -m pip install --force-reinstall dist/*.whl

python - <<'PY'
from opencc_py import converter
assert converter("cn", "tw2").convert("汉语") == "漢語"
PY

opencc-py --help
```

驗證完成後可清掉暫存檔：

```bash
deactivate 2>/dev/null || true
rm -rf .venv-release .venv-smoke build dist
```

## 3. 設定 PyPI Trusted Publisher

本專案使用 PyPI Trusted Publishing，不需要 PyPI API token。這是一次性設定，但必須在 PyPI 網站完成。

1. 登入 PyPI。
2. 進入 **Account settings**。
3. 進入 **Publishing**。
4. 選擇 **Add a new pending publisher**。
5. 填入以下資料：

| PyPI 欄位 | 值 |
| --- | --- |
| PyPI Project Name 專案名稱 | `opencc-py-tw2` |
| Owner 擁有者 | `doggy8088` |
| Repository name 儲存庫名稱 | `opencc-py` |
| Workflow name workflow 名稱 | `publish.yml` |
| Environment name 環境名稱 | `pypi` |

設定完成後，GitHub Actions 的 OIDC claim 會是：

```text
repo:doggy8088/opencc-py:environment:pypi
```

如果看到 `invalid-publisher`，通常代表 PyPI 端設定不匹配。請特別確認：

- Project name 專案名稱是 `opencc-py-tw2`，不是 `opencc-py`。
- Owner 擁有者是 `doggy8088`。
- Repository name 儲存庫名稱只填 `opencc-py`，不要填完整 URL。
- Workflow name 是 `publish.yml`，不是 `.github/workflows/publish.yml`。
- Environment name 環境名稱是 `pypi`。

## 4. 建立 GitHub Release

確認 CI 通過後，用 GitHub CLI 建立 release：

```bash
gh release create v0.1.0 \
  --repo doggy8088/opencc-py \
  --target main \
  --title "v0.1.0" \
  --notes "初始版本，依照 C# 實作移植為純 Python OpenCC。"
```

也可以在 GitHub 網頁操作：

1. 開啟 `https://github.com/doggy8088/opencc-py/releases/new`。
2. 建立 tag，例如 `v0.1.0`。
3. Target 目標選 `main`。
4. 填寫 release 標題與說明。
5. 按 **Publish release**。

發布 release 後，GitHub Actions 會自動執行 `publish.yml`。

## 5. 監看發布 workflow

```bash
gh run list --repo doggy8088/opencc-py --workflow publish.yml --limit 5
```

找到最新 run ID 後監看：

```bash
gh run watch <RUN_ID> --repo doggy8088/opencc-py --exit-status --interval 10
```

成功時，`Publish to PyPI` 步驟會完成，PyPI 會出現 `opencc-py-tw2` 的新版本。

## 6. 發布後驗證

等 PyPI 索引更新後，建立乾淨 venv 安裝：

```bash
python3 -m venv .venv-pypi-test
source .venv-pypi-test/bin/activate
python -m pip install --upgrade pip
python -m pip install --no-cache-dir opencc-py-tw2==0.1.0
```

確認 import 與 CLI：

```bash
python - <<'PY'
from opencc_py import converter
assert converter("cn", "tw2").convert("汉语") == "漢語"
print("opencc-py-tw2 OK")
PY

opencc-py --help
```

## 7. 如果發布失敗

### `invalid-publisher`

代表 PyPI 沒有找到符合 GitHub OIDC claims 的 Trusted Publisher。

處理方式：

1. 到 PyPI 的 **Account settings > Publishing**。
2. 確認 pending publisher 欄位完全符合第 3 節。
3. 如果設定錯誤，刪除錯的 pending publisher 後重建。
4. 刪除失敗的 GitHub Release/tag，再重建 release。

刪除失敗 release/tag：

```bash
gh release delete v0.1.0 --repo doggy8088/opencc-py --cleanup-tag --yes
git tag -d v0.1.0 2>/dev/null || true
```

重建 release 後 workflow 會重新發布。

### `File already exists`

代表同一個版本已經上傳到 PyPI。PyPI 不允許覆蓋既有版本。

處理方式：

1. 更新 `pyproject.toml` 版本，例如 `0.1.1`。
2. 提交並推送。
3. 建立新的 GitHub Release tag，例如 `v0.1.1`。

### 找不到 `opencc-py-tw2`

PyPI 索引可能還沒更新。等 1 到 2 分鐘後再試：

```bash
python -m pip install --no-cache-dir opencc-py-tw2==0.1.0
```

## 8. 發布檢查清單

- [ ] `pyproject.toml` 版本正確。
- [ ] `git status --short` 沒有未提交變更。
- [ ] 本機測試通過。
- [ ] `python -m build` 成功。
- [ ] `twine check dist/*` 成功。
- [ ] GitHub CI 通過。
- [ ] PyPI Trusted Publisher 設定為 `opencc-py-tw2`。
- [ ] GitHub Release tag 與版本一致。
- [ ] `publish.yml` 成功。
- [ ] 能從 PyPI 安裝並通過 smoke test。
