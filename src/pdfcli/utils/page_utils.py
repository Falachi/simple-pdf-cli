from contextlib import contextmanager
from functools import wraps
from pathlib import Path
from typing import List
from pypdf import PdfReader
import typer

from pdfcli.utils.validators import ensure_extension, exit_with_error_message, path_validator

# Returned a list without duplicates while in the same order based on the input.
def dedupe_ordered(numbers :List[int]) -> List[int]:
  seen = set()
  order_list = []

  for number in numbers:
    if number not in seen:
      seen.add(number)
      order_list.append(number)

  return order_list

# Add the remaining missing pages not in the page list.
def add_remaining_pages(page_numbers: List[int], total_pages: int) -> List[int]:
  seen = set(page_numbers)

  for page_number in range(total_pages):
    if page_number not in seen:
      page_numbers.append(page_number)
  
  return page_numbers

# Parse a page range string like '1-5,7,8,10-12,9' into a list of integers: [1,2,3,4,5,7,8,10,11,12,9]
def parse_page_ranges(pages: str, *, dups: bool = False, subtract_one: bool = False) -> List[int]:
  page_lst = []
  parts = [page.strip() for page in pages.strip(',').split(',')]

  # TODO: Create a validation function to check if the input is valid or need cleaning

  for part in parts:
    if "-" in part:
      start, end = part.split("-")
      start, end = int(start), int(end)

      if subtract_one:
        start -= 1
        end -= 1

      # If reorder is reversed
      if start > end: 
        page_lst.extend(range(start, end - 1, -1))
      else:
        page_lst.extend(range(start, end + 1))
    else:
      num = int(part)
      if subtract_one:
        num -= 1
      page_lst.append(num)
  
  if not dups:
    page_lst = dedupe_ordered(page_lst)

  return page_lst

# Create path by validating first
def create_path(path_name: str,*, default: str = "") -> str:

  path_name = path_name.strip()

  if not path_validator(path_name, default):
    exit_with_error_message("Path is invalid.")
  
  dir_path = Path(path_name)

  if dir_path.exists():
    if not typer.confirm("Folder already exist. Overwrite?"):
      raise typer.Exit(code=1)
  else:
    try:
      dir_path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
      exit_with_error_message('Permission denied.')
    except Exception as e:
      exit_with_error_message(e)
  
  return path_name # In case .strip() helps


def read_pdf(filename:str) -> PdfReader:
  path = ensure_extension(filename)
  reader = PdfReader(path)

  if reader.is_encrypted:
    password = typer.prompt(f"{file} is encrypted. Enter password")
    reader.decrypt(password)
  
  return PdfReader