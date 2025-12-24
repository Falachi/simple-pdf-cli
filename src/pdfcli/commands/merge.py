from typing import List
from pypdf import PdfWriter
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
import logging
from pathlib import Path

from pdfcli.utils.cli_utils import get_all_pdfs_in_folder, read_pdf_list
from pdfcli.utils.page_utils import check_output, read_pdf

description = """
  Merge multiple PDF files into one.\n
  Example:\n
    pdfcli merge file1.pdf file2.pdf -o merged.pdf
  """

def cli_execute(inputs: List[str], output: str) -> None:

  output = check_output(output)

  if len(inputs) == 1 and inputs[0].lower().endswith(".txt"):
    inputs = read_pdf_list(inputs[0])

  if inputs[0] == "." or inputs[0] == "./":
    inputs = get_all_pdfs_in_folder(".")
  
  with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    transient=True
  ) as progress:
    progress.add_task(description="Merging...", total=None)
    core_function([Path(i) for i in inputs], Path(output))
    
      
  rich.print(f"[green]Successfully merged into {output}[/green]")


def core_function(inputs: List[Path], output: Path) -> int:

  logging.getLogger("pypdf").setLevel(logging.ERROR) # Suppress pypdf warnings
  writer = PdfWriter()
  for pdf in inputs:
    pdf_path = str(pdf)
    reader = read_pdf(pdf_path)
    for page in reader.pages:
      writer.add_page(page)
  with open(str(output), "wb") as f:
    writer.write(f)

  return 0