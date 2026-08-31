import subprocess

def fetch_url(url: str) -> str:
    return subprocess.run(f"curl --silent {url}", shell=True, capture_output=True, text=True).stdout

