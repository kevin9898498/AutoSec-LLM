import subprocess

def show_git_ref(ref: str) -> str:
    return subprocess.run(f"git show {ref}", shell=True, capture_output=True, text=True).stdout

