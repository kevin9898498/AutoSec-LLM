# 批次評估與 Baseline 比較

`app.evaluate` 會對同一份受控測資跑兩個條件：

- `sast_guided`：將 Semgrep/Bandit 正規化後的 finding 提供給修復模型。
- `direct_repair`：模型只看原始碼與任務描述，自行檢查與修復；SAST 僅作為事後的獨立驗證，絕不傳入 repair prompt。

這是配對比較：同一題、同一 provider、同一個 `max_repairs`。預設離線 `DemoProvider` 只驗證管線可重現，不能用它的數據宣稱真實 LLM 的比較優勢；正式實驗請固定模型版本、溫度與 prompt，再使用 `--openai` 或接入本地模型。

## Manifest

專案的 benchmark manifest 格式如下（路徑可以相對 manifest 或專案根目錄）：

```json
{
  "version": "1.0",
  "language": "python",
  "cases": [
    {
      "id": "cwe89-001",
      "title": "SQLite f-string SQL injection",
      "prompt": "修復 SQLite 登入函式並維持功能",
      "cwe": "CWE-89",
      "severity": "HIGH",
      "vulnerable_path": "cases/cwe89-001/vulnerable.py",
      "secure_path": "cases/cwe89-001/secure.py",
      "test_path": "tests/cwe89-001_test.py",
      "expected_rule_ids": ["PY-SQLI-FSTRING"],
      "tags": ["sqlite", "sqli"]
    }
  ]
}
```

也支援 `expected_cwes`、`cwes`、`code` / `inline_code`、`source_path` 等常見別名，以及 JSONL；若環境有 PyYAML，也可讀 YAML。

## 執行

```powershell
python -m app.evaluate --manifest benchmark/manifest.json --output-dir evaluation-results
```

輸出一份不覆寫既有結果的時間戳 JSON 與 CSV。JSON 保留設定、完整 case-level audit 與摘要；CSV 每列為「一個 case × 一個策略」，可直接匯入 Excel 或 Plotly。

主要指標包括：

- 初始目標 CWE 是否被偵測（detection rate）
- 目標 finding 是否消失（target-removal rate）
- 最終語法正確率與 scanner-clean rate
- 靜態修復成功率（目標移除、語法通過、且無新 finding）
- 安全回歸率（最終出現初始沒有的 CWE/rule type）
- 平均 finding 數、修復輪數與延遲
- `sast_guided` 對 `direct_repair` 的 paired win/loss 與成功率差

## 可選 pytest 驗證

預設不執行程式碼。若要執行受控、已審查的 benchmark pytest：

```powershell
python -m app.evaluate --manifest benchmark/manifest.json --run-tests
```

每個測試必須從環境變數 `SECURE_REPAIR_TARGET` 讀取「暫存的修復後 Python 檔」路徑；評估器不會改寫 benchmark 原始檔。這個選項**不是隔離沙箱**，不可用來執行不可信的 LLM 程式碼；正式實驗應透過無網路、限時限資源的 Docker runner 執行。
