import subprocess

def search_audit_log(term: str) -> str:
    return subprocess.run(["grep", "-n", term, "audit.log"], shell=False, capture_output=True, text=True).stdout

