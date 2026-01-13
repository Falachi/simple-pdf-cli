from typing import Callable, List, Optional
from rich.console import Console
from pathlib import Path
from natsort import natsorted

from pdfcli.utils.validators import is_valid_image

console = Console()

def rprint(message: str,*, status: Optional[int] = None) -> None:

  styles = {
    0: "green",
    1: "red"
  }

  if status is None:
    console.print(message)
    return

  console.print(message, style=styles[status])


def default_extract_validator(path: str) -> bool:
  return path.lower().endswith(".pdf")

# Read all PDF files from a text file
def extract_lines_from_file(file_path: str, validator: Callable[[str], bool] = default_extract_validator) -> List[str]:

  paths = []
  current_line = ""
  try:
    with open(file_path, "r") as f:
      for line in f:
        line = line.strip()
        current_line = line
        if line and validator(line):
          paths.append(line)
        else:
          rprint(f"Skipping invalid entry '{line}' from {file_path}", status=1)
  except OSError as e:
    rprint(f"Failed while reading entry '{current_line}' from {file_path}: {e}", status=1)
    return []
  
  return paths

def get_all_pdfs_in_folder(folder_path: str) -> List[str]:

  path = Path(folder_path)
  if not path.is_dir():
    rprint(f"{folder_path} is not a valid directory. Skipping folder.", status=1)
    return []
  
  pdfs = [str(file) for file in path.glob("*.pdf") if file.is_file()]
  if not pdfs:
    rprint(f"No PDF files found in {folder_path}.", status=1)
    return []

  pdfs = natsorted(pdfs)
  
  rprint(f"Found {len(pdfs)} PDF files in {folder_path}.")

  return pdfs

def get_all_images_in_folder(folder_path: str) -> List[str]:

  path = Path(folder_path)
  if not path.is_dir():
    rprint(f"{folder_path} is not a valid directory. Skipping folder.", status=1)
    return []
  
  images = []
  
  for file in path.iterdir():
    if file.is_file() and is_valid_image(str(file)):
      images.append(str(file))

  if not images:
    rprint(f"No image files found in {folder_path}. Skipping folder.", status=1)
    return []

  images = natsorted(images)
  
  rprint(f"Found {len(images)} image files in {folder_path}.")

  return images