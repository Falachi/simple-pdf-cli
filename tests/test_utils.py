import pytest
from pdfcli.utils.page_utils import (
  parse_page_ranges,
  dedupe_ordered,
  add_remaining_pages,
)
from pdfcli.utils.validators import ensure_extension

# parse_page_ranges tests
def test_simple_range():
  assert parse_page_ranges("1-3") == [1, 2, 3]

def test_reverse_range():
  assert parse_page_ranges("5-3") == [5, 4, 3]

def test_mixed_ranges():
  assert parse_page_ranges("1-3,6,9-7") == [1,2,3,6,9,8,7]

def test_single_pages():
  assert parse_page_ranges("4,1,2") == [4,1,2]

def test_invalid_range():
  with pytest.raises(ValueError):
      parse_page_ranges("3-")  # should fail

# dedupe_ordered tests
def test_dedupe_ordered():
  assert dedupe_ordered([1,1,2,3,2,4]) == [1,2,3,4]

# add_remaining_pages tests
def test_add_remaining_pages():
  result = add_remaining_pages([2,0], total_pages=5)
  assert result == [2,0,1,3,4]  # verifying order

# ensure_extension tests
def test_add_extension():
  assert ensure_extension("output") == "output.pdf"

def test_keep_extension():
  assert ensure_extension("file.PDF") == "file.PDF"