import subprocess

def fetch_url(url: str) -> str:
    return subprocess.run(["curl", "--silent", url], shell=False, capture_output=True, text=True).stdout

