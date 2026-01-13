# Images to PDF
from PIL import Image
from typing import List
from pathlib import Path
from pdf2image import convert_from_path
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn

from pdfcli.utils.cli_utils import extract_lines_from_file, get_all_images_in_folder
from pdfcli.utils.page_utils import check_output, create_path, get_pdf_password, is_poppler_available
from pdfcli.utils.validators import exit_with_error_message, is_valid_image, input_validator

img2pdf_desc = """
  Convert images to a single PDF.\n
  Order of input images determines the page order. Supports mixing individual files, .txt files containing image paths, and folders containing images.\n
  Example:\n
  pdfcli image1.png image2.png image3.png -o output.pdf
  """

def normalize_inputs(images: List[str]) -> List[str]: 
  valid_images = []
  
  for item in images:
    path = Path(item)

    if not path.exists():
      exit_with_error_message(f"Path not found: {item}")
    
    if path.is_dir():
      valid_images.extend(get_all_images_in_folder(str(path)))
    
    if path.is_file():
      if item.lower().endswith(".txt"):
        valid_images.extend(extract_lines_from_file(str(path), validator=is_valid_image))
      elif is_valid_image(item):
        valid_images.append(str(path))
      else:
        exit_with_error_message(f"Unsupported file type: {item}")
  
  return valid_images

def img2pdf_execution(images: List[str], output: str) -> None:
    
  pil_images = []
  output = check_output(output)
  images = normalize_inputs(images)

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

def warning_message_poppler_missing() -> str:
  if is_poppler_available():
    return ""
  return "[yellow][bold]WARNING:[/bold] Poppler not found. PDF to image conversion will not work.[/yellow]"

pdf2img_desc = f"""
  Convert each PDF page into a PNG.\n
  The page order determines the image order.\n
  Example:\n
  pdfcli file.pdf -o out_images 
  """

def pdf2img_execution(input: str, output_folder: str) -> None:

  input = input_validator(input)
  password = get_pdf_password(input) # in case the file is protected
  
  output_folder = create_path(output_folder, default="out_images")
  pages = convert_from_path(input, userpw=password)

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