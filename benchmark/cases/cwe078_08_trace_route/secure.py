import subprocess

def trace_route(target: str) -> str:
    return subprocess.run(["traceroute", target], shell=False, capture_output=True, text=True).stdout

