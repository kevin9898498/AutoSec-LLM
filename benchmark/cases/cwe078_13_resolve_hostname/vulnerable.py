import subprocess

def resolve_hostname(host: str) -> str:
    return subprocess.run(f"host {host}", shell=True, capture_output=True, text=True).stdout

