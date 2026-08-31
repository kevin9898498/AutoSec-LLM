import subprocess

def ping_host(host: str) -> str:
    return subprocess.run(["ping", "-c", "1", host], shell=False, capture_output=True, text=True).stdout

