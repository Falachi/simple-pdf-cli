
from pypdf import PdfWriter
from pdfcli.utils.page_utils import read_pdf


description = """
Encrypt the PDF with a password.\n
Supports RC4-40, RC4-128, AES-128, AES-256-R5, and AES-256. Default to AES-256-R5.
Example:\n
pdfcli encrpyt file.pdf -a AES-256-R5
"""

DEFAULT_ALGORITHM = "AES-256-R5"

def execute(input: str, output: str, algorithm: str, overwrite: bool) -> None:

  reader = read_pdf(input)
  writer = PdfWriter(clone_from=reader)

  writer.encrypt()
