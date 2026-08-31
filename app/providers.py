import os
import re
from abc import ABC, abstractmethod
from typing import Any, List


class LLMProvider(ABC):

  @abstractmethod
  def generate(self, prompt: str) -> str:
    pass

  @abstractmethod
  def repair(
      self, code: str, findings: List[Any], prompt: str = ""
  ) -> str:
    pass


def extract_python_code(text: str) -> str:
  """精準提取 Markdown 內的純 Python 程式碼"""
  match = re.search(r"```(?:python)?\s*(.*?)\s*```", text, re.DOTALL)
  if match:
    return match.group(1).strip()
  return text.strip()


class OfflineProvider(LLMProvider):
  """離線規則式精準修復"""

  def generate(self, prompt: str) -> str:
    return (
        "import sqlite3\n\n"
        "def check_user_login(username: str, password_hash: str) -> bool:\n"
        '    conn = sqlite3.connect("users.db")\n'
        "    cursor = conn.cursor()\n"
        '    sql_query = f"SELECT id FROM users WHERE username = \'{username}\''
        ' AND password = \'{password_hash}\'"\n'
        "    cursor.execute(sql_query)\n"
        "    user = cursor.fetchone()\n"
        "    conn.close()\n"
        "    return user is not None\n"
    )

  def repair(
      self, code: str, findings: List[Any], prompt: str = ""
  ) -> str:
    # 離線修復 CWE-89 (SQL Injection)
    if "SELECT" in code and ("f'" in code or 'f"' in code):
      return (
          "import sqlite3\n\n"
          "def check_user_login(username: str, password_hash: str) ->"
          " bool:\n"
          '    conn = sqlite3.connect("users.db")\n'
          "    cursor = conn.cursor()\n"
          '    sql_query = "SELECT id FROM users WHERE username = ? AND'
          ' password = ?"\n'
          "    cursor.execute(sql_query, (username, password_hash))\n"
          "    user = cursor.fetchone()\n"
          "    conn.close()\n"
          "    return user is not None\n"
      )

    # 離線修復 CWE-78 (Command Injection)
    if "os.system" in code or "ping" in code:
      return (
          "import subprocess\n\n"
          "def check_server_status(hostname: str) -> int:\n"
          '    """透過 ping 指令安全檢查遠端主機狀態"""\n'
          '    res = subprocess.run(["ping", "-c", "1", hostname],'
          " capture_output=True, text=True)\n"
          "    return res.returncode\n"
      )

    return code


class OpenAIProvider(LLMProvider):

  def __init__(self) -> None:
    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
      raise ValueError("OPENAI_API_KEY is required for OpenAI mode.")

    self.client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    self.model = "gemini-3.6-flash"

  def generate(self, prompt: str) -> str:
    response = self.client.chat.completions.create(
        model=self.model,
        messages=[
            {
                "role": "system",
                "content": "You are a secure coding assistant. Return ONLY valid Python code.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
    )
    return extract_python_code(response.choices[0].message.content or "")

  def repair(
      self, code: str, findings: List[Any], prompt: str = ""
  ) -> str:
    issues = "\n".join([
        f"- Line {getattr(f, 'line', '?')}: [{getattr(f, 'cwe', 'Issue')}] {getattr(f, 'message', '')}"
        for f in findings
    ])
    user_msg = (
        f"Original Task: {prompt}\n\n"
        f"Code with Vulnerabilities:\n```python\n{code}\n```\n\n"
        f"SAST Findings:\n{issues}\n\n"
        "Security Fix Requirements:\n"
        "1. Remove `os.system` and unsafe string formatting completely.\n"
        "2. Use `subprocess.run([...], check=False)` with argument lists"
        " (shell=False).\n"
        "3. Output ONLY the clean, full repaired Python code inside ```python"
        " ... ```."
    )
    response = self.client.chat.completions.create(
        model=self.model,
        messages=[
            {
                "role": "system",
                "content": "You are an automated secure code refactoring engine. Return ONLY the final repaired code block.",
            },
            {"role": "user", "content": user_msg},
        ],
        temperature=0.1,
    )
    return extract_python_code(response.choices[0].message.content or "")


def get_provider(use_openai: bool = False) -> LLMProvider:
  return OpenAIProvider() if use_openai else OfflineProvider()