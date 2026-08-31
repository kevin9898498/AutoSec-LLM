import subprocess

def list_archive(archive: str) -> str:
    return subprocess.run(["tar", "-tf", archive], shell=False, capture_output=True, text=True).stdout

