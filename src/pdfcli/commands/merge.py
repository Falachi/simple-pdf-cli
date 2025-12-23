from typing import List
from pypdf import PdfWriter
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
import logging



from pdfcli.utils.page_utils import check_output, read_pdf

description = """
  Merge multiple PDF files into one.\n
  Example:\n
    pdfcli merge file1.pdf file2.pdf -o merged.pdf
  """

def execute(inputs: List[str], output: str) -> None:

  logging.getLogger("pypdf").setLevel(logging.ERROR)
  writer = PdfWriter()
  output = check_output(output)
  
  with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    transient=True
  ) as progress:
    progress.add_task(description="Merging...", total=None)
    for pdf in inputs:
      reader = read_pdf(pdf)
      for page in reader.pages:
        writer.add_page(page)
    with open(output, "wb") as f:
      writer.write(f)
      
  rich.print(f"[green]Successfully merged into {output}[/green]")