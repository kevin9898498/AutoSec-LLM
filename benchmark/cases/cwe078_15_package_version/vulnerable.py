import subprocess

def package_version(package: str) -> str:
    return subprocess.run(f"pip show {package}", shell=True, capture_output=True, text=True).stdout

