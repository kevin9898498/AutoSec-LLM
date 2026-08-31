import subprocess

def package_version(package: str) -> str:
    return subprocess.run(["pip", "show", package], shell=False, capture_output=True, text=True).stdout

