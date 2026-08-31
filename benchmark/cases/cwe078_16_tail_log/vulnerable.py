import subprocess

def tail_log(path: str) -> str:
    return subprocess.run(f"tail -n 10 {path}", shell=True, capture_output=True, text=True).stdout

