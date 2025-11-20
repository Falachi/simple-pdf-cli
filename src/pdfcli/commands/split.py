from pathlib import Path
from pypdf import PdfReader, PdfWriter
import rich

from pdfcli.utils import parse_page_ranges


description= """
Split the PDF into multiple PDFs.\n
Separate a page or a range from the main PDF. Pages can repeat for each split. Does not support reverse pages, or compiling different pages into one. Use the 'trim' function instead.\n
Separate each split with a comma (,).\n
Example (will create 3 PDFs):\n
pdfcli split input.pdf -o out_pdfs -p 1-5,3-6,7\n
"""

# Split PDF
def execute(input: str, output_folder: str, parts: str) -> None:

  if not output_folder.strip():
    output_folder = "out_pdfs"
  Path(output_folder).mkdir(exist_ok=True) # TODO: Proper folder name verification

  reader = PdfReader(input)

  groupings = [parse_page_ranges(part, subtract_one=True, dups=False) for part in parts.split(',')]

  for index, pages in enumerate(groupings, start=1):
    writer = PdfWriter()
    for page in pages:
      writer.add_page(reader.pages[page])
    writer.write(f"{output_folder}/output-{index}.pdf")
  
  rich.print(f"[green]Successfully split into {output_folder}/[/green]")
