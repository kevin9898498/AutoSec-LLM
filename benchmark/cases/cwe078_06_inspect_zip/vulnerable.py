import subprocess

def inspect_zip(archive: str) -> str:
    return subprocess.run(f"zipinfo {archive}", shell=True, capture_output=True, text=True).stdout

