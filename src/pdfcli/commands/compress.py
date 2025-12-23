from pathlib import Path
from pypdf import PdfWriter
from pdfcli.utils.cli_utils import rprint
from pdfcli.utils.page_utils import check_output, read_pdf
from rich.progress import Progress, SpinnerColumn, TextColumn

from pdfcli.utils.validators import exit_with_error_message

description = """
Compress a PDF file into a smaller size.

This command supports both lossless and lossy compression:

• Lossless compression is controlled by the --level option (0-9).\n
0 = no compression, 9 = maximum lossless compression.\n\n

• Lossy image compression is controlled by the --quality option.\n
You may use a preset (listed below) or a numeric JPEG quality value (100-1),
where 100 keeps the original quality and 1 is the lowest quality.\n\n

If neither --level nor --quality is provided, defaults are used:\n
level = 6, quality = medium.\n\n

Quality presets:\n
[lossless, high, medium, low, verylow]\n\n

Example:\n
pdfcli compress input.pdf -o output.pdf --level 6 --quality medium

"""

QUALITY_PRESET = {
  "lossless": None,
  "high": 85,
  "medium": 70,
  "low": 50,
  "verylow": 30
}

def execute(file_input: str, output: str, level: int = 6, quality: str = "medium") -> None:

  output = check_output(output)
  reader = read_pdf(file_input)

  try:
    q = int(quality)
    if 1 <= q <= 100:
      quality_value = q
    else:
      raise ValueError
  except ValueError:
    if quality not in QUALITY_PRESET:
      exit_with_error_message(f"Invalid quality preset: {quality}")
    quality_value = QUALITY_PRESET[quality]

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
        if quality_value is not None:
          for img in page.images:
            img.replace(img.image, quality=quality_value)
        page.compress_content_streams(level=level)

      with open(output, "wb") as f:
        writer.write(f)
      
    except Exception as e:
      exit_with_error_message(f"Failed to compress PDF: {e}")
  
  completion_message(file_input, output)

def completion_message(input_path: str, output_path: str) -> None:

  input_size = Path(input_path).stat().st_size
  output_size = Path(output_path).stat().st_size

  percentage_reduced = round((1 - output_size / input_size) * 100)

  rprint(f"Successfully reduced file size by {percentage_reduced}%", status=0)

