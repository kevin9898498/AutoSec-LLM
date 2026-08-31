import subprocess

def tail_log(path: str) -> str:
    return subprocess.run(["tail", "-n", "10", path], shell=False, capture_output=True, text=True).stdout

