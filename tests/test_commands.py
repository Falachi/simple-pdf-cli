import operator
from pathlib import Path
from pypdf import PdfReader
from typer.testing import CliRunner
import shutil

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
PDF_SAMPLE_40MB = str(BASE / "data" / "input" / "40mb.pdf")

EXPECTED_MERGE = str(BASE / "data" / "expected" / "merge.pdf")
EXPECTED_IMG2PDF = str(BASE / "data" / "expected" / "img2pdf.pdf")
EXPECTED_PDF2IMG = str(BASE / "data" / "expected" / "out-img")
EXPECTED_REORDER = str(BASE / "data" / "expected" / "reorder.pdf")
EXPECTED_TRIM = str(BASE / "data" / "expected" / "trim.pdf")
EXPECTED_SPLIT = str(BASE / "data" / "expected" / "split")
EXPECTED_ENCRYPT = str(BASE / "data" / "expected" / "encrypt.pdf")
EXPECTED_DECRYPT = str(BASE / "data" / "expected" / "decrypt.pdf")

ENCRYPTION_PASSWORD = "12345"

def assert_pdf(pdf_path: str, expected_pdf_path: str, 
              *, validate_page_count: bool = True, 
              expected_page_count: int | None = None,
              password: str | None = None,
              expected_file_password: str | None = None,
              ) -> bool:

  file_reader = PdfReader(pdf_path)
  expected_reader = PdfReader(expected_pdf_path)

  expected_file_password = (
    expected_file_password
    if expected_file_password is not None
    else password
  )

  if file_reader.is_encrypted:
    indicator = file_reader.decrypt(password)
    print(f"Indicator!!! {indicator}")
    if indicator == 0:
      raise Exception("Wrong password.")
  
  if expected_reader.is_encrypted:
    indicator = expected_reader.decrypt(expected_file_password)
    print(f"Indicator!!! {indicator}")
    if indicator == 0:
      raise Exception("Wrong password.")

  expected_page_count = (
    expected_page_count
    if expected_page_count is not None
    else len(expected_reader.pages)
  )

  if validate_page_count and len(file_reader.pages) != expected_page_count:
    return False

  for index in range(len(file_reader.pages)):
    if not file_reader.pages[index].mediabox.width == expected_reader.pages[index].mediabox.width:
      return False
    if not file_reader.pages[index].mediabox.height == expected_reader.pages[index].mediabox.height:
      return False

  return True

def assert_folder_content(folder_path: str, expected_folder_path:str, *, file_ext: str) -> bool:

  testing_path = Path(folder_path)
  expected_path = Path(expected_folder_path)

  testing_files = sorted(p.name for p in testing_path.glob(f"*{file_ext}"))
  expected_files = sorted(p.name for p in expected_path.glob(f"*{file_ext}"))

  testing_file_count = sum(1 for _ in testing_path.glob(f"*{file_ext}"))
  expected_file_count = sum(1 for _ in expected_path.glob(f"*{file_ext}"))

  if testing_file_count != expected_file_count:
    return False
  
  if testing_files != expected_files:
    return False
  
  #NOTE: put more folder assertions? not sure what else to check

  return True

def compare_file_size(folder_path: str, expected_path: str, *, comparison: str = "<") -> bool:

  OPS = {
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
    "==": operator.eq,
    "!=": operator.ne,
  }

  op = OPS[comparison]

  if op is None:
    raise ValueError(f"Invalid comparison operator: {comparison}")

  file_size = Path(folder_path).stat().st_size
  expected_size = Path(expected_path).stat().st_size

  return op(file_size, expected_size)


# test if the app can just run
def test_app():
  result = runner.invoke(app)
  assert result.exit_code == 0

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

    print(output)
    print(result.output)
    if result.exception:
      print(result.exception)
      print(type(result.exception))
    
    assert result.exit_code == 0
    assert output.exists()
    assert assert_folder_content(output_str, EXPECTED_PDF2IMG, file_ext=".png")

class TestTrimCommand:

  output_name = "trim.pdf"

  def test_trim_help(self):
    result = runner.invoke(app, ['trim', '--help'])
    assert result.exit_code == 0

  def test_trim(self, tmp_path: Path):
    output = tmp_path / self.output_name
    output_str = str(output)

    result = runner.invoke(app, [
      "trim",
      PDF_SAMPLE_8_PAGE,
      "--output",
      output_str,
      "--page",
      "5-6,3,1,8-5"
    ])

    print(result.output)
    if result.exception:
      print(result.exception)
      print(type(result.exception))
    
    assert result.exit_code == 0
    assert output.exists()
    assert assert_pdf(output_str, EXPECTED_TRIM)

class TestReorderCommand:

  output_name = "reorder.pdf"

  def test_reorder_help(self):
    result = runner.invoke(app, ['reorder', '--help'])
    assert result.exit_code == 0

  def test_reorder(self, tmp_path: Path):
    output = tmp_path / self.output_name
    output_str = str(output)

    result = runner.invoke(app, [
      "reorder",
      PDF_SAMPLE_8_PAGE,
      "--output",
      output_str,
      "--order",
      "4,3,2,5,7,8,1"
    ])

    print(result.output)
    if result.exception:
      print(result.exception)
      print(type(result.exception))
    
    assert result.exit_code == 0
    assert output.exists()
    assert assert_pdf(output_str, EXPECTED_REORDER)

class TestSplitCommand:

  output_name = "split"

  def test_split_help(self):
    result = runner.invoke(app, ['split', '--help'])
    assert result.exit_code == 0

  def test_split(self, tmp_path: Path):
    output = tmp_path / self.output_name
    output_str = str(output)

    result = runner.invoke(app, [
      "split",
      PDF_SAMPLE_8_PAGE,
      "--output",
      output_str,
      "--part",
      "1,5-8,3-4"
    ])

    print(result.output)
    if result.exception:
      print(result.exception)
      print(type(result.exception))
    
    assert result.exit_code == 0
    assert output.exists()
    assert assert_folder_content(output_str, EXPECTED_SPLIT, file_ext=".pdf")

class TesteEncryptCommand:

  output_name = "encrypt.pdf"

  def test_encrypt_help(self):
    result = runner.invoke(app, ['encrypt', '--help'])
    assert result.exit_code == 0

  def test_encrypt(self, tmp_path: Path):
    output = tmp_path / self.output_name
    output_str = str(output)

    result = runner.invoke(app, [
      "encrypt",
      PDF_SAMPLE_8_PAGE,
      "--output",
      output_str,
      "--password",
      ENCRYPTION_PASSWORD
    ])

    print(result.output)
    if result.exception:
      print(result.exception)
      print(type(result.exception))
    
    assert result.exit_code == 0
    assert output.exists()
    assert assert_pdf(output_str, EXPECTED_ENCRYPT, password=ENCRYPTION_PASSWORD)

  def test_remove_after(self, tmp_path: Path):
    output_name = "encrypt-rm_test.pdf"
    output = tmp_path / output_name
    output_str = str(output)

    copied_file_name = "copy-encryption-test.pdf"
    copy_to = tmp_path / copied_file_name

    shutil.copyfile(PDF_SAMPLE_8_PAGE, str(copy_to))

    result = runner.invoke(app, [
      "encrypt",
      str(copy_to),
      "--output",
      output_str,
      "--password",
      ENCRYPTION_PASSWORD,
      "--remove-source"
    ])

    print(result.output)
    if result.exception:
      print(result.exception)
      print(type(result.exception))
    
    assert result.exit_code == 0
    assert output.exists()
    assert not copy_to.exists() # check if file is removed or not

class TesteDecryptCommand:

  output_name = "decrypt.pdf"

  def test_decrypt_help(self):
    result = runner.invoke(app, ['decrypt', '--help'])
    assert result.exit_code == 0

  def test_decrypt(self, tmp_path: Path):
    output = tmp_path / self.output_name
    output_str = str(output)

    result = runner.invoke(app, [
      "decrypt",
      PDF_SAMPLE_PROTECTED,
      "--output",
      output_str,
      "--password",
      ENCRYPTION_PASSWORD
    ])

    print(result.output)
    if result.exception:
      print(result.exception)
      print(type(result.exception))
    
    assert result.exit_code == 0
    assert output.exists()
    assert assert_pdf(output_str, EXPECTED_DECRYPT, password=ENCRYPTION_PASSWORD)

  def test_remove_after(self, tmp_path: Path):
    output_name = "decrypt-rm_test.pdf"
    output = tmp_path / output_name
    output_str = str(output)

    copied_file_name = "copy-decryption-test.pdf"
    copy_to = tmp_path / copied_file_name

    shutil.copyfile(PDF_SAMPLE_PROTECTED, str(copy_to))

    result = runner.invoke(app, [
      "decrypt",
      str(copy_to),
      "--output",
      output_str,
      "--password",
      ENCRYPTION_PASSWORD,
      "--remove-source"
    ])

    print(result.output)
    if result.exception:
      print(result.exception)
      print(type(result.exception))
    
    assert result.exit_code == 0
    assert output.exists()
    assert not copy_to.exists() # check if file is removed or not

class TesteCompressCommand:

  output_name = "compress.pdf"

  

  def test_compress_help(self):
    result = runner.invoke(app, ['compress', '--help'])
    assert result.exit_code == 0

  def test_compress(self, tmp_path: Path):
    output = tmp_path / self.output_name
    output_str = str(output)

    result = runner.invoke(app, [
      "compress",
      PDF_SAMPLE_40MB,
      "--output",
      output_str,
      "--level",
      6,
      "--quality",
      "medium"
    ])

    print(result.output)
    if result.exception:
      print(result.exception)
      print(type(result.exception))
    
    assert result.exit_code == 0
    assert output.exists()
    assert compare_file_size(PDF_SAMPLE_40MB, output_str, comparison=">")
    