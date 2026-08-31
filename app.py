from __future__ import annotations

import difflib
import os
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))
from app.pipeline import run_pipeline
from app.providers import get_provider

st.set_page_config(page_title="LLM Secure Repair", layout="wide")
st.title("LLM 程式碼漏洞偵測與自動修復")
st.caption("生成 → 語法驗證 → SAST → 定點修復 → 二次驗證。結果僅供開發輔助，不能保證程式安全。")

with st.sidebar:
  st.header("執行設定")
  mode = st.radio("Provider", ["Offline demo", "OpenAI API"])
  max_repairs = st.slider("最大修復輪數", 0, 3, 2)

  if mode == "Offline demo":
    st.info("離線模式使用可重現的弱點範例與規則式修復，可立即 Demo。")
  else:
    st.info("OpenAI 模式使用雲端 LLM 進行即時修復（需配置 API Key）。")

prompt = st.text_input("任務需求", "撰寫一個從 SQLite 讀取使用者的登入驗證函數")
code = st.text_area("可選：直接貼上要檢測的 Python 程式碼", height=250,
                    placeholder="留白時由 Provider 生成；貼上後會直接進入閉環修復。")

if st.button("開始掃描與修復", type="primary"):
    try:
        provider = get_provider(mode == "OpenAI API")
        with st.spinner("執行閉環管線中…"):
            result = run_pipeline(prompt, provider, code or None, max_repairs)
        st.session_state.result = result
    except Exception as exc:
        st.error(str(exc))

result = st.session_state.get("result")
if result:
    if result.status == "PASS":
        st.success(result.message)
    else:
        st.warning(result.message)

    metrics = st.columns(4)
    metrics[0].metric("狀態", result.status)
    metrics[1].metric("修復輪數", max(0, len(result.attempts) - 1))
    metrics[2].metric("初始 finding", len(result.original_findings))
    metrics[3].metric("最終 finding", len(result.final_findings))

    left, right = st.columns(2)
    with left:
        st.subheader("原始程式碼")
        st.code(result.original_code, language="python")
    with right:
        st.subheader("最終程式碼")
        st.code(result.final_code, language="python")

    st.subheader("Unified Diff")
    diff = "\n".join(difflib.unified_diff(result.original_code.splitlines(), result.final_code.splitlines(),
                                              fromfile="original.py", tofile="repaired.py", lineterm=""))
    st.code(diff or "沒有變更", language="diff")

    rows = []
    for attempt in result.attempts:
        for finding in attempt.scan.findings:
            rows.append({"attempt": attempt.number, "tool": finding.tool, "CWE": finding.cwe or "N/A",
                         "severity": finding.severity.value, "line": finding.start_line,
                         "message": finding.message, "excerpt": finding.code_excerpt})
    st.subheader("漏洞結果")
    if rows:
        frame = pd.DataFrame(rows)
        st.dataframe(frame, use_container_width=True, hide_index=True)
        chart = frame.groupby(["attempt", "severity"]).size().reset_index(name="count")
        st.plotly_chart(px.bar(chart, x="attempt", y="count", color="severity", barmode="group",
                              title="各輪掃描 finding 數"), use_container_width=True)
    else:
        st.info("沒有偵測到 finding。")

    with st.expander("每輪驗證紀錄"):
        for attempt in result.attempts:
            st.write({"attempt": attempt.number, "syntax_valid": attempt.syntax.valid,
                      "syntax_error": attempt.syntax.error, "tools": attempt.scan.tools_used,
                      "scanner_errors": attempt.scan.errors, "note": attempt.note})
