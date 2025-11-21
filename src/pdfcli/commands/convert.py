# Images to PDF
from PIL import Image
from typing import List
from pdf2image import convert_from_path
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn

from pdfcli.utils.page_utils import create_path
from pdfcli.utils.validators import ensure_extension

img2pdf_desc = """
  Convert images to a single PDF.\n
  Order of input images determines the page order.\n
  Example:\n
  pdfcli image1.png image2.png image3.png -o output.pdf
  """

def img2pdf_execution(images: List[str], output: str) -> None:
    
  pil_images = []
  output = ensure_extension(output)

  with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    transient=True
  ) as progress:
    progress.add_task(description="Converting...", total=None)
    for img in images:
      im = Image.open(img)
      if im.mode == "RGBA":
        im = im.convert("RGB")
      pil_images.append(im)

    first = pil_images[0]
    rest = pil_images[1:]

    first.save(output, save_all=True, append_images=rest)

  rich.print(f"[green]Created PDF {output}[/green]")

# PDF to Images

pdf2img_desc = """
  Convert each PDF page into a PNG.\n
  The page order determines the image order.\n
  Example:\n
  pdfcli file.pdf -o out_images 
  """

def pdf2img_execution(input: str, output_folder: str) -> None:

  input = ensure_extension(input)
  
  output_folder = create_path(output_folder, default="out_images")
  pages = convert_from_path(input)

  with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    transient=True
  ) as progress:
    progress.add_task(description="Converting...", total=None)
    for i, page in enumerate(pages):
      out_path = f"{output_folder}/page_{i+1}.png"
      page.save(out_path, "PNG")

  rich.print(f"[green]Images saved to {output_folder}/[/green]")