import subprocess

def list_directory(path: str) -> str:
    return subprocess.run(f"ls -la {path}", shell=True, capture_output=True, text=True).stdout

