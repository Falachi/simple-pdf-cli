from typing import List
import typer
from typing_extensions import Annotated

from pdfcli import __version__
from pdfcli.commands import compress, merge, convert, reorder, trim, split, decrypt, encrypt
from pdfcli.utils.cli_utils import read_pdf_list, get_all_pdfs_in_folder

app = typer.Typer(help=
  """A simple PDF CLI tool.\n
  Easily merge PDFs, convert between PDF and images, rearrage PDF pages, and trim a PDF.\n
  Supports batch processing with a .txt file containing PDF paths, or a folder containing PDFs. The latter will sort PDFs alphabetically.\n
  Run 'pdfcli [command] --help' for specific command help.
  """
  )

# Commands

# Merge PDFs
@app.command(help=merge.description, name="merge")
def merge_command(inputs: Annotated[List[str], typer.Argument(help="Input PDF files. Space-separated. Use quotes for paths with spaces.")],
  output: Annotated[str, typer.Option(
      ...,"-o", "--output", help="Output PDF file (path + filename).",
      prompt="Output file name"
  )],
  batch: Annotated[bool, typer.Option(
    ..., "--batch", "-b", help="Merge all PDFs in the input folder.",
  )] = False):

  if batch or len(inputs) == 1 and inputs[0].lower().endswith(".txt"):
    inputs = read_pdf_list(inputs[0])
  
  if inputs[0] == "." or inputs[0] == "./":
    inputs = get_all_pdfs_in_folder(".")

  merge.execute(inputs, output)

# Images to PDF
@app.command(help=convert.img2pdf_desc, name="img2pdf")
def img2pdf_command(images: Annotated[List[str], typer.Argument(help="Input image files. Space-separated. Use quotes for paths with spaces.")], 
  output: Annotated[str, typer.Option(
      ..., "-o", "--output", help="Output PDF file (path + filename).",
      prompt="Output file name"
  )]):

  convert.img2pdf_execution(images, output)

# PDF to images
@app.command(help=convert.pdf2img_desc, name="pdf2img")
def pdf2img_command(input: Annotated[str, typer.Argument(help="Input PDF file. Use quotes for path with spaces.")],
  output_folder: Annotated[str, typer.Option(
    ..., "-o", "--output", help="Output file location.",
    prompt="Output folder name"
    )] = "out_images"):
  
  convert.pdf2img_execution(input, output_folder)

# Reorder PDF pages
@app.command(help=reorder.description, name="reorder")
def reorder_command(input: Annotated[str, typer.Argument(help="Input PDF file. Use quotes for path with spaces.")],
  output: Annotated[str, typer.Option(
    ..., "-o", "--output", help="Output PDF file (path + filename).",
    prompt="Output file name"
    )],
  order: Annotated[str, typer.Option(
    ..., "-r", "--order", help="Order of input files by their index",
    prompt="Pages order (e.g: 3,1,2)"
  )]):

  reorder.execute(input, output, order)

# Trim PDF
@app.command(help=trim.description, name="trim")
def trim_command(input: Annotated[str, typer.Argument(help="Input PDF file. Use quotes for path with spaces.")],
  output: Annotated[str, typer.Option(
    ..., "-o", "--output", help="Output PDF file (path + filename).",
    prompt="Output file name"
    )],
  pages: Annotated[str, typer.Option(
    ..., "-p", "--page", help="Pages to keep. Please don't add any spaces. e.g. '1-5,7,10-12,9'",
    prompt="Pages (e.g. 1-5,7,10-12,9)"
  )]):

  trim.execute(input, output, pages)

# Split PDF
@app.command(help=split.description, name="split")
def split_command(input: Annotated[str, typer.Argument(help="Input PDF file. Use quotes for path with spaces.")],
  parts: Annotated[str, typer.Option(
    ..., "--part","-p",
    help="Page or range to split. Please don't add any spaces. e.g '1-5,3-6,7'",
    prompt= "Parts (e.g 1-5,3-6,7)"
    )],
  output_folder: Annotated[str, typer.Option(
    ..., "-o", "--output", help="Output file location.",
    prompt="Output folder name"
    )] = "out_pdfs"):
  
  split.execute(input, output_folder, parts)

# Encrypt PDF
@app.command(help=encrypt.description, name="encrypt")
def encrypt_command(input: Annotated[str, typer.Argument(help="Input PDF file. Use quotes for path with spaces.")],
  output: Annotated[str, typer.Option(
    ..., "-o", "--output", help="Output PDF file (path + filename).",
    prompt="Output file name"
    )],
  password: Annotated[str, typer.Option(
    ..., "-p", "--password", help="The password use to encrypt the file. Use quotes if password has whitespace. No restriction.",
    prompt=True,
    confirmation_prompt=True,
    hide_input=True
    )],
  algorithm: Annotated[str, typer.Option(
    ..., "-a", "--algorithm", help="The algorithm use for encryption.",
    )] = encrypt.DEFAULT_ALGORITHM,
  remove_source: Annotated[bool, typer.Option(
    ..., "-rm", "--remove-source", help="Remove the original PDF after processing.",
    metavar="remove-source",
  )] = False):
  
  encrypt.execute(input, output, password, algorithm, remove_source)

# Decrypt PDF
@app.command(help=decrypt.description, name="decrypt")
def decrypt_command(input: Annotated[str, typer.Argument(help="Input PDF file. Use quotes for path with spaces.")],
  output: Annotated[str, typer.Option(
    ..., "-o", "--output", help="Output PDF file (path + filename).",
    prompt="Output file name"
    )],
  password: Annotated[str, typer.Option(
    ..., "-p", "--password", help="The password to read and decrypt the PDF. Use quotes if password has whitespace.",
    prompt=True,
    hide_input=True
    )],
  remove_source: Annotated[bool, typer.Option(
    ..., "-rm", "--remove-source", help="Remove the original PDF after processing.",
    metavar="remove-source",
  )] = False):
  
  decrypt.execute(input, output, password, remove_source)

# Compress PDF
@app.command(help=compress.description, name="compress")
def compress_command(input: Annotated[str, typer.Argument(help="Input PDF files. Space-separated. Use quotes for paths with spaces.")],
  output: Annotated[str, typer.Option(
      ...,"-o", "--output", help="Output PDF file (path + filename).",
      prompt="Output file name"
  )],
  quality: Annotated[str, typer.Option(
    ...,"--quality","-q", 
    help="The quality of images in the PDF. Can be set with presets or value. Check description for more info.",
  )] = "medium",
  level: Annotated[int, typer.Option(
    ...,"--level","-l", 
    help="Level of compression. Range is between 0 to 9, where 0 is no compression, and 9 is highest compression.",
  )] = 6,
  ):
  
  compress.execute(input, output, level, quality)

@app.callback(invoke_without_command=True)
def main(version: Annotated[bool, typer.Option(
  "--version", "-v", help="Show version and exit", callback=False, is_eager=True # type: ignore
  )] = False): # type: ignore

  if version:
    print(f"pdfcli version {__version__}")
    raise typer.Exit()