import subprocess

def checksum_file(path: str) -> str:
    return subprocess.run(["sha256sum", path], shell=False, capture_output=True, text=True).stdout

