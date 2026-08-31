import subprocess

def list_archive(archive: str) -> str:
    return subprocess.run(f"tar -tf {archive}", shell=True, capture_output=True, text=True).stdout

