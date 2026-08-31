import subprocess

def resolve_domain(domain: str) -> str:
    return subprocess.run(["nslookup", domain], shell=False, capture_output=True, text=True).stdout

