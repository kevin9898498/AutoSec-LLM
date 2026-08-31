import subprocess

def checksum_file(path: str) -> str:
    return subprocess.run(f"sha256sum {path}", shell=True, capture_output=True, text=True).stdout

