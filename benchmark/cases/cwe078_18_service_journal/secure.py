import subprocess

def service_journal(service: str) -> str:
    return subprocess.run(["journalctl", "-u", service], shell=False, capture_output=True, text=True).stdout

