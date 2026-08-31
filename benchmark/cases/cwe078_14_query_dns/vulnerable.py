import subprocess

def query_dns(domain: str) -> str:
    return subprocess.run(f"dig {domain}", shell=True, capture_output=True, text=True).stdout

