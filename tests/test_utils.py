from pathlib import Path
from pypdf import PdfReader
import pytest
from pdfcli.utils.page_utils import parse_page_ranges, dedupe_ordered, add_remaining_pages
from pdfcli.utils.validators import ensure_extension, page_validator, path_validator
from typer.testing import CliRunner

from pdfcli.main import app

runner = CliRunner()

BASE = Path(__file__).parent

PDF_SAMPLE_8_PAGE = str(BASE / "data" / "input" / "8pages.pdf")
PDF_SAMPLE_1_PAGE_1 = str(BASE / "data" / "input" / "1page-1.pdf")
PDF_SAMPLE_1_PAGE_2 = str(BASE / "data" / "input" / "1page-2.pdf")
IMAGE_SAMPLE_1 = str(BASE / "data" / "input" / "photo1.jpg")
IMAGE_SAMPLE_2 = str(BASE / "data" / "input" / "photo2.jpg")
IMAGE_SAMPLE_3 = str(BASE / "data" / "input" / "photo3.jpg")
PDF_SAMPLE_PROTECTED = str(BASE / "data" / "input" / "protected.pdf")

EXPECTED_MERGE = str(BASE / "data" / "expected" / "merge.pdf")
EXPECTED_IMG2PDF = str(BASE / "data" / "expected" / "img2pdf.pdf")
EXPECTED_PDF2IMG = str(BASE / "data" / "expected" / "out-img")
EXPECTED_REORDER = str(BASE / "data" / "expected" / "reorder.pdf")
EXPECTED_TRIM = str(BASE / "data" / "expected" / "trim.pdf")
EXPECTED_SPLIT = str(BASE / "data" / "expected" / "split")
EXPECTED_ENCRYPT = str(BASE / "data" / "expected" / "encrypt.pdf")
EXPECTED_DECRYPT = str(BASE / "data" / "expected" / "decrypt.pdf")

ENCRYPTION_PASSWORD = "12345"

# assert pdf
def assert_pdf(file: str, expected: str) -> bool:

  assertion = True

  file_reader = PdfReader(file)
  expected_reader = PdfReader(expected)

  if not len(file_reader.pages) == len(expected_reader.pages):
    assertion = False

  for index in range(len(file_reader.pages)):
    if not file_reader.pages[index].mediabox.width == expected_reader.pages[index].mediabox.width:
      assertion = False
    if not file_reader.pages[index].mediabox.height == expected_reader.pages[index].mediabox.height:
      assertion = False

  return assertion

def assert_folder_files(folder: str, expected_folder: str, *, limit_to: str) -> bool:
  return True

# test if the app can just run
def test_app():
  result = runner.invoke(app)
  assert result.exit_code == 0

# test merge
class TestMergeCommand:

  output_name = "merge.pdf"

  def test_merge_help(self):
    result = runner.invoke(app, ['merge', '--help'])
    assert result.exit_code == 0

  def test_merge(self, tmp_path: Path):
    output = tmp_path / self.output_name
    output_str = str(output)

    result = runner.invoke(app, [
       'merge', 
       PDF_SAMPLE_1_PAGE_1,
       PDF_SAMPLE_1_PAGE_2,
       '--output', 
       output_str
    ])

    print(result.output)
    if result.exception:
      print(result.exception)
      print(type(result.exception))

    assert result.exit_code == 0
    assert output.exists()
    assert assert_pdf(output_str, EXPECTED_MERGE)

# test img2pdf
class TestImg2PdfCommand:

  output_name = "img2pdf.pdf"

  def test_img2pdf_help(self):
    result = runner.invoke(app, ['pdf2img', '--help'])
    assert result.exit_code == 0

  def test_img2pdf(self, tmp_path: Path):
    output = tmp_path / self.output_name
    output_str = str(output)

    result = runner.invoke(app, [
       "img2pdf",
       IMAGE_SAMPLE_1,
       IMAGE_SAMPLE_2,
       IMAGE_SAMPLE_3,
       "--output",
       output_str
    ])

    print(result.output)
    if result.exception:
      print(result.exception)
      print(type(result.exception))
    
    assert result.exit_code == 0
    assert output.exists()
    assert assert_pdf(output_str, EXPECTED_IMG2PDF)

# test img2pdf
class TestPdf2ImgCommand:

  output_name = "out-img"

  def test_pdf2img_help(self):
    result = runner.invoke(app, ['pdf2img', '--help'])
    assert result.exit_code == 0

  def test_pdf2img(self, tmp_path: Path):
    output = tmp_path / self.output_name
    output_str = str(output)

    result = runner.invoke(app, [
       'pdf2img',
       PDF_SAMPLE_8_PAGE,
       "--output",
       output_str
    ])

    input_reader = PdfReader(PDF_SAMPLE_8_PAGE)

    output_file_count = sum(1 for _ in output.glob("*.png"))

    print(output)
    print(result.output)
    if result.exception:
      print(result.exception)
      print(type(result.exception))
    
    assert result.exit_code == 0
    assert output.exists()
    assert len(input_reader.pages) == output_file_count
  

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