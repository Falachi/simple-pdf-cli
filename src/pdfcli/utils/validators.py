
# File validation and correction
import re
import rich
from pathlib import Path

import typer

INVALID_CHARS = r'\\|/|:|\*|\?|"|<|>|\|'

def ensure_extension(filename: str, extension: str = ".pdf") -> str:

  filename = filename.strip()

  if is_valid_filename(filename, no_ext=False):
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

# Folder validation
def path_validator(path_name: str) -> bool:

  if not path_name:
    return False
  