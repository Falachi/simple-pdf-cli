from typing import List
import typer
from typing_extensions import Annotated

from . import __version__
import pdfcli.commands.merge as merge
import pdfcli.commands.convert as convert
import pdfcli.commands.reorder as reorder
import pdfcli.commands.trim as trim

app = typer.Typer(help=
  """A simple PDF CLI tool.\n
  Easily merge PDFs, convert between PDF and images, rearrage PDF pages, and trim a PDF.\n
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
  )]):

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

@app.callback(invoke_without_command=True)
def main(version: Annotated[bool, typer.Option(
  "--version", "-v", help="Show version and exit", callback=False, is_eager=True
  )] = False):

  if version:
    print(f"pdfcli version {__version__}")
    raise typer.Exit()