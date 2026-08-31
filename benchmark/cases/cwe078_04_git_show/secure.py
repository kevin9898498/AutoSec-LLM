import subprocess

def show_git_ref(ref: str) -> str:
    return subprocess.run(["git", "show", ref], shell=False, capture_output=True, text=True).stdout

