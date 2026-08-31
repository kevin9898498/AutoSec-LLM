import subprocess

def network_interface(interface: str) -> str:
    return subprocess.run(["ip", "link", "show", interface], shell=False, capture_output=True, text=True).stdout

