import rich
import typer
from pypdf import PdfReader, PdfWriter
from typing_extensions import Annotated

from pdfcli.utils import add_remaining_pages, ensure_extension, parse_page_ranges

description = """
  Reorder PDF pages.\n
  Duplicates are ignored, only the first occurance is used. Pages not specified in the order will be appended at the end in their original sequence.
  Use "trim" instead if you want to keep only the specified pages.\n
  Example:\n
  pdfcli input.pdf -o output.pdf -r 3,1,2
  """


# Reorder PDF
def execute(input: str, output: str, order: str) -> None:

  reader = PdfReader(input)
  writer = PdfWriter()

  output = ensure_extension(output)
  total_pages = len(reader.pages)
  page_order = add_remaining_pages(
    parse_page_ranges(order, subtract_one=True),
    total_pages)

  for idx in page_order:
    writer.add_page(reader.pages[idx])

  with open(output, "wb") as f:
    writer.write(f)
  rich.print(f"[green]Reordered and saved to {output}[/green]")