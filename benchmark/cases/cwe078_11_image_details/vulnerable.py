import subprocess

def image_details(path: str) -> str:
    return subprocess.run(f"identify {path}", shell=True, capture_output=True, text=True).stdout

