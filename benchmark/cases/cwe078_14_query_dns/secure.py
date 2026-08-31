import subprocess

def query_dns(domain: str) -> str:
    return subprocess.run(["dig", domain], shell=False, capture_output=True, text=True).stdout

