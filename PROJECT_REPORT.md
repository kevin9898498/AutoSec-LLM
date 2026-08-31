# 專題設計摘要：LLM 程式碼漏洞偵測與自動修復

## 研究問題

對已知的 Python 安全弱點，結合靜態掃描器與 LLM 的閉環管線，能否在**不破壞既有功能**的前提下，提高漏洞修復率？本系統不主張以掃描結果取代人工安全審查。

## 系統模組

1. **Code generation / ingestion**：接收任務 prompt 或貼上的 Python 程式碼。
2. **Syntax gate**：以 `ast.parse` 與 `compile()` 拒絕不可解析的結果。
3. **SAST adapter**：執行 Semgrep、Bandit，轉為統一的 `Finding` schema。
4. **Repair provider**：將 finding、原始碼與保留介面限制送給 LLM，要求僅回傳完整程式碼。
5. **Verification and presentation**：再次驗證、Diff、統計與審計紀錄。

```text
Prompt / Code → Syntax gate → SAST → Repair prompt → Syntax gate → SAST → Report
                                  ↑                         │
                                  └──── retry, max 2 ────────┘
```

## 本 MVP 的範圍

- 語言：Python 單檔。
- 初始 CWE：CWE-89（SQL injection）、CWE-78（command injection）、CWE-798（hard-coded credentials）。
- 迴圈上限：兩輪修復；超過後輸出 `NEEDS_REVIEW`，不可靜默宣稱成功。
- 預設不執行被修復程式碼。若加入 pytest 回歸測試，必須放入無網路、資源受限的容器。

## 評估指標

| 指標 | 定義 |
|---|---|
| 偵測率 | 已知弱點測資中，至少被一項啟用規則偵測的比例 |
| 修復成功率 | 目標 finding 消失、語法檢查與功能測試均成功的比例 |
| 功能回歸率 | 修復後 pytest 失敗的比例 |
| 安全回歸率 | 修復後出現新 finding 的比例 |
| 效率 | 每題耗時、API token/成本、平均修復輪數 |

## 6 週時程

| 項目 | W1 | W2 | W3 | W4 | W5 | W6 |
|---|---|---|---|---|---|---|
| 定義 CWE、測資與成功條件 | ■ |  |  |  |  |  |
| SAST adapter 與 Finding schema | ■ | ■ |  |  |  |  |
| LLM 生成、修復與 retry 管線 |  | ■ | ■ |  |  |  |
| pytest 測資與隔離執行 |  |  | ■ | ■ |  |  |
| Streamlit 與批次評估 |  |  |  | ■ | ■ |  |
| 實驗、報告、Demo 彩排 |  |  |  |  | ■ | ■ |
