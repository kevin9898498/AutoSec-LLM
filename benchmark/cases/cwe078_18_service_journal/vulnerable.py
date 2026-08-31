import subprocess

def service_journal(service: str) -> str:
    return subprocess.run(f"journalctl -u {service}", shell=True, capture_output=True, text=True).stdout

