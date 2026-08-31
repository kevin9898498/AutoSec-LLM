# LLM Secure Repair MVP

一個 Python 專題 MVP：**生成 → 語法驗證 → 靜態掃描 → LLM 定點修復 → 二次驗證**。

> 這是開發輔助與研究原型，不是安全保證。真正部署前仍須人工 code review、依賴套件掃描與隔離執行測試。

## 功能

- Semgrep + Bandit SAST 整合；未安裝時仍以內建 demo 規則偵測 CWE-89、CWE-78、CWE-798。
- Pydantic 統一所有掃描結果為 `Finding`。
- `ast.parse` + `compile()` 語法閘門。
- 最多 N 次修復、修復後再次語法與 SAST 檢查。
- Streamlit 介面顯示程式碼、Diff、漏洞表格與趨勢圖。
- 預設離線 Demo；設定 API key 後可切換 OpenAI provider。

## 安裝與執行

```powershell
cd C:\Users\user\Documents\Codex\2026-08-20\https-share-gemini-google-nlevkhwjmf8h-https\outputs\llm-secure-repair-mvp
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

CLI 離線 Demo：

```powershell
python -m app.cli --prompt "撰寫 SQLite 登入函數"
python -m app.cli --code samples\vulnerable_login.py
pytest -q
```

使用 OpenAI API 時，複製 `.env.example` 的值到環境變數（勿將金鑰提交到 Git）：

```powershell
$env:OPENAI_API_KEY = "..."
$env:OPENAI_MODEL = "gpt-4o-mini"
python -m app.cli --openai
```

## 管線與接受條件

```text
Prompt / 手動程式碼 → Syntax gate → Semgrep + Bandit → Repair → Syntax gate → Scan → UI
```

通過條件：程式可編譯，且沒有任何啟用的 SAST finding。實際專題評測時，應再加入每題專屬 `pytest` 功能回歸測試；不要把「掃描器沒有報警」解讀為完全安全。

## 建議的下一步

1. 擴充 50–60 組含預期 CWE 與 pytest 的受控測資。
2. 將檢測結果統一輸出為 SARIF，方便日後串接 GitHub Actions。
3. 若要執行不可信的回歸測試，使用無網路、限時限資源的 Docker 容器。
4. 量測修復成功率、功能回歸率、新增漏洞率、成本、延遲與平均修復輪數。
