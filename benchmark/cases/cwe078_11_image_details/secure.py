import subprocess

def image_details(path: str) -> str:
    return subprocess.run(["identify", path], shell=False, capture_output=True, text=True).stdout

