import subprocess

def resolve_domain(domain: str) -> str:
    return subprocess.run(f"nslookup {domain}", shell=True, capture_output=True, text=True).stdout

