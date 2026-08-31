import subprocess

def list_directory(path: str) -> str:
    return subprocess.run(["ls", "-la", path], shell=False, capture_output=True, text=True).stdout

