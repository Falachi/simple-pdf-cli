from typing import List
from pypdf import PdfWriter
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
import logging
from pathlib import Path

from pdfcli.utils.cli_utils import get_all_pdfs_in_folder, extract_lines_from_file
from pdfcli.utils.page_utils import check_output, read_pdf
from pdfcli.utils.validators import exit_with_error_message

description = """
  Merge multiple PDF files into one.\n
  Supports merging from individual files, a .txt file containing PDF paths, or a folder containing PDFs.\n
  Supports mixing these input types.\n
  Example:\n
    pdfcli merge file1.pdf file2.pdf -o merged.pdf
  """

def normalize_inputs(inputs: List[str]) -> List[str]:
  pdfs = []

  for item in inputs:
    path = Path(item)

    if not path.exists():
      exit_with_error_message(f"Path not found: {item}")
    
    if path.is_dir():
      pdfs.extend(get_all_pdfs_in_folder(str(path)))
    
    if path.is_file():
      if item.lower().endswith(".txt"):
        pdfs.extend(extract_lines_from_file(str(path)))
      elif item.lower().endswith(".pdf"):
        pdfs.append(str(path))
      else:
        exit_with_error_message(f"Unsupported file type: {item}")
  
  return pdfs

def cli_execute(inputs: List[str], output: str) -> None:

  output = check_output(output)
  inputs = normalize_inputs(inputs)
  
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