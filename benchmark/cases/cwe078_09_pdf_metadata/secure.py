import subprocess

def pdf_metadata(document: str) -> str:
    return subprocess.run(["pdfinfo", document], shell=False, capture_output=True, text=True).stdout

