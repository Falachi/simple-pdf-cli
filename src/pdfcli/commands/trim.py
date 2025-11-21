
from pypdf import PdfReader, PdfWriter
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn

from pdfcli.utils.page_utils import parse_page_ranges
from pdfcli.utils.validators import ensure_extension, exit_with_error_message, page_validator

description = """
  Trim or reorder pages of a PDF using page range syntax.\n
  Support ranges and specific pages such as "1-5" or "1,2,3". It can also reverse pages like "9-5", or "9, 6, 7", and reorder pages. Duplicates are allowed.\n
  Please specify without using spaces.\n
  Example:\n
  pdfcli input.pdf -o output.pdf -p 1-5,7,10-12,9
  """

# Trim PDFs
def execute(input: str, output: str, pages: str) -> None:
  
  reader =  PdfReader(input)
  writer = PdfWriter()

  page_order = parse_page_ranges(pages, dups=True, subtract_one=True)
  output = ensure_extension(output)

  if not page_validator(page_order,len(reader.pages)):
    exit_with_error_message("Page is out of range.")
  
  with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    transient=True
  ) as progress:
    progress.add_task(description="Trimming...", total=None)
    for idx in page_order:
      writer.add_page(reader.pages[idx])

    with open(output, "wb") as f:
      writer.write(f)
      
  rich.print(f"[green]Trimmed and saved to {output}[/green]")