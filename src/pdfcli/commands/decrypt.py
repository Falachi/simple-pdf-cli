from pypdf import PdfWriter
import rich
from pdfcli.utils.page_utils import check_output, read_pdf
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path

from pdfcli.utils.validators import exit_with_error_message

description = """
Decrypt a PDF. Requires the password.\n
For privacy, omit writing the password with the flag.\n
Example:\n
pdfcli decrypt file.pdf -o output.pdf -p password1
"""

def execute(input: str, output: str, password: str, remove_source: bool = False) -> None:

  output = check_output(output)
  reader = read_pdf(input, password=password)
  
  with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    transient=True
  ) as progress:
    progress.add_task(description="Decrypting...", total=None)

    try:
      writer = PdfWriter(clone_from=reader)

      if reader.metadata: # preserve metadata
        writer.add_metadata(reader.metadata)
      
      with open(output, "wb") as f:
        writer.write(f)
    except Exception as e:
      exit_with_error_message(f"Failed to decrypt PDF: {e}")
    
    if remove_source:
      Path(input).unlink()

  rich.print(f"[green]Decrypted and saved to {output}[/green]")