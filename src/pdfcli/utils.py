from typing import List

# File validation and correction
def ensure_extension(filename: str, extension: str = ".pdf") -> str:
  if not filename.lower().endswith(extension):
    return filename + extension
  return filename

# Returned a list without duplicates while in the same order based on the input.
def dedupe_ordered(numbers :List[int]) -> List[int]:
  seen = set()
  order_list = []

  for number in numbers:
    if number not in seen:
      seen.add(number)
      order_list.append(number)

  return order_list

# Add the remaining missing pages not in the page list. Mutates the list in-place.
def add_remaining_pages(page_numbers: List[int], total_pages: int) -> None:
  seen = set(page_numbers)

  for page_number in range(total_pages):
    if page_number not in seen:
      page_numbers.append(page_number)

# Parse a page range string like '1-5,7,8,10-12,9' into a list of integers: [1,2,3,4,5,7,8,10,11,12,9]
def parse_page_ranges(pages: str) -> List[int]:
    page_lst = []
    parts = [page.strip() for page in pages.strip(',').split(',')]

    for part in parts:
        if "-" in part:
            start, end = part.split("-")
            start, end = int(start), int(end)

            # If reorder is reversed
            if start > end: 
                page_lst.extend(range(start, end - 1, -1))
            else:
                page_lst.extend(range(start, end + 1))
        else:
            page_lst.append(int(part))

    return page_lst