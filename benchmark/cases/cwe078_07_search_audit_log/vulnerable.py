import subprocess

def search_audit_log(term: str) -> str:
    return subprocess.run(f"grep -n {term} audit.log", shell=True, capture_output=True, text=True).stdout

