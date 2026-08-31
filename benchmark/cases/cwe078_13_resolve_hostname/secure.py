import subprocess

def resolve_hostname(host: str) -> str:
    return subprocess.run(["host", host], shell=False, capture_output=True, text=True).stdout

