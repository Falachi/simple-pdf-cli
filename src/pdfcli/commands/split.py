from pypdf import PdfWriter
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn

from pdfcli.utils.page_utils import create_path, parse_page_ranges, read_pdf
from pdfcli.utils.validators import exit_with_error_message, page_validator


description= """
Split the PDF into multiple PDFs.\n
Separate a page or a range from the main PDF. Pages can repeat for each split. Does not support reverse pages, or compiling different pages into one. Use the 'trim' function instead.\n
Separate each split with a comma (,).\n
Example (will create 3 PDFs):\n
pdfcli split input.pdf -o out_pdfs -p 1-5,3-6,7\n
"""

# Split PDF
def execute(input: str, output_folder: str, parts: str) -> None:

  output_folder = create_path(output_folder, default="out_pdfs")

  reader = read_pdf(input)

  groupings = [parse_page_ranges(part, subtract_one=True, dups=False) for part in parts.split(',')]

  for group in groupings:
    if not page_validator(group, len(reader.pages)):
      exit_with_error_message("Page is out of range.")

  with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    transient=True
  ) as progress:
    progress.add_task(description="Splitting...", total=None)
    for index, pages in enumerate(groupings, start=1):
      writer = PdfWriter()
      for page in pages:
        writer.add_page(reader.pages[page])
      writer.write(f"{output_folder}/output-{index}.pdf")
  
  rich.print(f"[green]Successfully split into {output_folder}/[/green]")
