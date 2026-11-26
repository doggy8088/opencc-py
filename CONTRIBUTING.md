# 貢獻與驗證

## 本機與 CI 驗證分工

- 啟用本機 pre-commit hook（每個 clone 設定一次）：`git config core.hooksPath .githooks`
- 分工原則：本機負責 format 與快速回歸；CI 負責完整測試矩陣與「乾淨環境」驗證。hook 只放快檢查，慢測試一律交給 CI，避免被 `--no-verify` 繞過。
- 本機 hook：unittest 全套（數秒）。
- CI：`ci.yml` 跑 Python 3.11／3.12／3.13 矩陣＋build＋smoke test，以 CI 為準。
