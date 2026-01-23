

from pypdf import PdfReader
from pdfcli.utils.cli_utils import create_and_print_metadata_table
from pdfcli.utils.page_utils import read_pdf

description = "Manage PDF metadata"

REG_FIELDS = {
  "Title": "title",
  "Author": "author",
  "Subject": "subject",
  "Creation Date": "creation_date",
  "Modification Date": "modification_date",
  "Keywords": "keywords",
}

def get_all_metadata(reader: PdfReader) -> dict:
  metadata = reader.metadata
  xmp_meta = reader.xmp_metadata
  
  meta_dict = {
    label: getattr(metadata, attr, "") or ""
    for label, attr in REG_FIELDS.items()
  }

  if xmp_meta:
    print(xmp_meta.dc_title)
    print(xmp_meta.dc_creator)
    print(xmp_meta.dc_description)
    print(xmp_meta.dc_subject)
    print(xmp_meta.dc_publisher)
    print(xmp_meta.xmp_create_date)
    print(xmp_meta.xmp_modify_date)
    print(xmp_meta.pdf_keywords)
  
  return meta_dict

def execute(input: str, is_edit: bool) -> None:
  
  reader = read_pdf(input)
  reg_metadata = get_all_metadata(reader)
  
  create_and_print_metadata_table(reg_metadata)
