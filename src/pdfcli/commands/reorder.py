import rich
from pypdf import PdfWriter
from rich.progress import Progress, SpinnerColumn, TextColumn

from pdfcli.utils.page_utils import add_remaining_pages, check_output, parse_page_ranges, read_pdf
from pdfcli.utils.validators import exit_with_error_message, page_validator

description = """
  Reorder PDF pages.\n
  Duplicates are ignored, only the first occurance is used. Pages not specified in the order will be appended at the end in their original sequence.
  Use "trim" instead if you want to keep only the specified pages.\n
  Example:\n
  pdfcli input.pdf -o output.pdf -r 3,1,2
  """


# Reorder PDF
def execute(input: str, output: str, order: str) -> None:

  reader = read_pdf(input)
  writer = PdfWriter()

  output = check_output(output)
  total_pages = len(reader.pages)
  page_order = add_remaining_pages(
    parse_page_ranges(order, subtract_one=True),
    total_pages)

  if not page_validator(page_order, total_pages):
    exit_with_error_message("Page is out of range.")

  with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    transient=True
  ) as progress:
    progress.add_task(description="Changing orders...", total=None)
    for idx in page_order:
      writer.add_page(reader.pages[idx])

    with open(output, "wb") as f:
      writer.write(f)

  rich.print(f"[green]Reordered and saved to {output}[/green]")