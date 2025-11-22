
from pypdf import PdfWriter
import rich
from pdfcli.utils.page_utils import check_output, read_pdf
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path

from pdfcli.utils.validators import exit_with_error_message

description = """
Encrypt the PDF with a password.\n
For privacy, omit writing the password with the flag. Supports RC4-40, RC4-128, AES-128, AES-256-R5, and AES-256. Default to AES-256-R5.\n
Example:\n
pdfcli encrpyt file.pdf -a AES-256-R5
"""

DEFAULT_ALGORITHM = "AES-256-R5"

def execute(input: str, output: str, password: str, 
  algorithm: str = DEFAULT_ALGORITHM, remove_source: bool = False) -> None:

  output = check_output(output)

  reader = read_pdf(input)
  
  with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    transient=True
  ) as progress:
    progress.add_task(description="Encrpyting...", total=None)

    try:
      writer = PdfWriter(clone_from=reader)
      writer.encrypt(password, algorithm=algorithm)

      if reader.metadata: # preserve metadata
        writer.add_metadata(reader.metadata)
      
      with open(output, "wb") as f:
        writer.write(f)
    except Exception as e:
      exit_with_error_message(f"Failed to encrypt PDF: {e}")
    
    if remove_source:
      Path(input).unlink()

  rich.print(f"[green]Encrypted and saved to {output}[/green]")
