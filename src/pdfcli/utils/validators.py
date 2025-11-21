
# File validation and correction
import re
from typing import List
import rich
from pathlib import Path

import typer

INVALID_CHARS = r'\\|/|:|\*|\?|"|<|>|\|'

def ensure_extension(filename: str, *, extension: str = ".pdf") -> str:

  filename = filename.strip()

  if not is_valid_filename(filename, no_ext=False):
    exit_with_error_message("File name invalid.")
  
  if not filename.lower().endswith(extension):
    return filename + extension
  return filename

def exit_with_error_message(reason: str) -> None:
  rich.print(f"[red]Error! {reason}\nPlease check and try again.[/red]")
  raise typer.Exit(code=1)

def is_valid_filename(name: str, *, no_empty = True, no_ext = True, no_char = True) -> bool:
  name = name.strip()
  if not name and no_empty:
    return False
  if no_ext and name.endswith(".") or name.endswith(" "):
    return False
  if no_char and re.search(INVALID_CHARS, name):
    return False
  
  return True

WINDOWS_RESERVED = {
  "CON", "PRN", "AUX", "NUL",
  *(f"COM{i}" for i in range(1, 10)),
  *(f"LPT{i}" for i in range(1, 10))
}


# Folder validation
def path_validator(path_name: str, default: str = "") -> bool:
  path_name = path_name.strip()

  if not path_name:
    if not default:
      return False
    else:
      path_name = default

  parts = path_name.replace("\\", "/").split("/")

  for part in parts:
    if not part:
      continue
    if part.upper() in WINDOWS_RESERVED:
      return False
    
    if part.endswith(".") or part.endswith(" "):  # Windows rule
      return False
    
    if re.search(INVALID_CHARS, part):
      return False
  
  return True

# assumes the list is 0-indexed
def page_validator(pages: List[int], total_pages: int) -> bool:

  if not pages:
    return False

  if min(pages) < 0 or max(pages) >= total_pages:
    return False
  
  return True