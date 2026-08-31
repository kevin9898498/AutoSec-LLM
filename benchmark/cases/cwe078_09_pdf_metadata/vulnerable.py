import subprocess

def pdf_metadata(document: str) -> str:
    return subprocess.run(f"pdfinfo {document}", shell=True, capture_output=True, text=True).stdout

