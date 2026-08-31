import subprocess

def inspect_zip(archive: str) -> str:
    return subprocess.run(["zipinfo", archive], shell=False, capture_output=True, text=True).stdout

