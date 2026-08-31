import subprocess

def trace_route(target: str) -> str:
    return subprocess.run(f"traceroute {target}", shell=True, capture_output=True, text=True).stdout

