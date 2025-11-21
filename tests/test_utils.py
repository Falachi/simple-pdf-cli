import pytest
from pdfcli.utils.page_utils import parse_page_ranges, dedupe_ordered, add_remaining_pages
from pdfcli.utils.validators import ensure_extension, page_validator, path_validator

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

# page_validator tests
def test_valid_pages_within_range():
  assert page_validator([0, 1, 2, 3], total_pages=10) is True

def test_single_page_edge_zero():
  assert page_validator([0], total_pages=5) is True

def test_single_page_edge_max():
  assert page_validator([10], total_pages=10) is False

def test_page_below_zero():
  assert page_validator([-1, 2, 3], total_pages=10) is False

def test_page_above_total():
  assert page_validator([0, 2, 11], total_pages=10) is False

def test_empty_list_should_fail():
  assert page_validator([], total_pages=10) is False  # optional depending on your logic

def test_large_valid_input():
  assert page_validator(list(range(0, 500)), total_pages=500) is True

def test_large_invalid_input():
  assert page_validator(list(range(0, 750)), total_pages=500) is False

# path_validator tests
def test_standard_folder_name():
    assert path_validator("Documents") is True

def test_nested_path():
    assert path_validator("foo/bar/baz") is True

def test_trailing_dot():
    assert path_validator("folder.") is False

def test_windows_reserved_name():
    assert path_validator("CON") is False  # NUL, AUX, LPT1 also invalid

def test_invalid_characters():
    assert path_validator("my|folder") is False

def test_empty_string():
    assert path_validator("") is False

def test_spaces_are_trimmed():
    assert path_validator("   folder   ") is True

def test_forward_and_backslashes():
    assert path_validator("foo\\bar/baz") is True