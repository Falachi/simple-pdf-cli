from pathlib import Path
from pypdf import PdfWriter
from pdfcli.utils.cli_utils import rprint
from pdfcli.utils.page_utils import check_output, read_pdf
from rich.progress import Progress, SpinnerColumn, TextColumn

from pdfcli.utils.validators import exit_with_error_message

description = """
Compress a PDF file into a smaller size.\n
Example:\n
pdfcli compress input.pdf -o output.pdf -l 5
"""

def execute(file_input: str, output: str, level: int = 5) -> None:

  output = check_output(output)
  reader = read_pdf(file_input)

  if level not in range(0, 10):
    exit_with_error_message(f"Level is outside of range. Accepted range is 0 - 9.")

  with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    transient=True
  ) as progress:
    progress.add_task(description="Compressing...", total=None)

    try:
      writer = PdfWriter(clone_from=reader)

      if reader.metadata:
        writer.add_metadata(reader.metadata)
      
      # removing duplicates
      writer.compress_identical_objects(remove_identicals=True, remove_orphans=True)

      # lossless compression
      for page in writer.pages:
        page.compress_content_streams(level=level)

      with open(output, "wb") as f:
        writer.write(f)
      
      completion_message(file_input, output)
    except Exception as e:
      exit_with_error_message(f"Failed to compress PDF: {e}")

def completion_message(input_path: str, output_path: str) -> str:

  input_size = Path(input_path).stat().st_size
  output_size = Path(output_path).stat().st_size

  percentage_reduced = round((output_size / input_size) * 100, 2)

  rprint(f"Successfully reduced file size by {percentage_reduced}.", status=0)

