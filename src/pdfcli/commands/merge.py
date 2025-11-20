from typing import List
from pypdf import PdfReader, PdfWriter
import rich

from pdfcli.utils import ensure_extension

description = """
  Merge multiple PDF files into one.\n
  Example:\n
    pdfcli merge file1.pdf file2.pdf -o merged.pdf
  """

def execute(inputs: List[str], output: str) -> None:

  writer = PdfWriter()
  output = ensure_extension(output)

  for pdf in inputs:
    reader = PdfReader(pdf)
    for page in reader.pages:
      writer.add_page(page)
  with open(output, "wb") as f:
    writer.write(f)
  rich.print(f"[green]Successfully merged into {output}[/green]")