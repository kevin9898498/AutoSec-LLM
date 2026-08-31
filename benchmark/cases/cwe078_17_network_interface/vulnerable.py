import subprocess

def network_interface(interface: str) -> str:
    return subprocess.run(f"ip link show {interface}", shell=True, capture_output=True, text=True).stdout

