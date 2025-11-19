from typing import List
import typer
from typing_extensions import Annotated
import rich
from pypdf import PdfReader, PdfWriter
from PIL import Image
from pdf2image import convert_from_path
from pathlib import Path
from pdfcli.utils import parse_page_ranges, dedupe_ordered, add_remaining_pages, ensure_extension

app = typer.Typer(help="""A simple PDF CLI tool.
\nEasily merge PDFs, convert between PDF and images, and rearrage PDF pages. Run 'pdfcli [command] --help' for specific command help.""")

# Merge PDFs
@app.command()
def merge(inputs: Annotated[List[str], typer.Argument(help="Input PDF files. Space-separated. Use quotes for paths with spaces.")],
        output: Annotated[str, typer.Option(
            ...,"-o", "--output", help="Output PDF file (path + filename).",
            prompt="Output file name"
        )]):
    
    """
    Merge multiple PDF files into one.\n
    Example:\n
      pdfcli merge file1.pdf file2.pdf -o merged.pdf
    """

    writer = PdfWriter()
    output = ensure_extension(output)

    for pdf in inputs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            writer.add_page(page)
    with open(output, "wb") as f:
        writer.write(f)
    rich.print(f"[green]Successfully merged into {output}[/green]")

# Images to PDF
@app.command()
def img2pdf(images: Annotated[List[str], typer.Argument(help="Input image files. Space-separated. Use quotes for paths with spaces.")], 
        output: Annotated[str, typer.Option(
            ..., "-o", "--output", help="Output PDF file (path + filename).",
            prompt="Output file name"
        )]):
    
    """
    Convert images to a single PDF. Order of input images determines the page order.\n
    Example:\n
    pdfcli image1.png image2.png image3.png -o output.pdf
    """

    pil_images = []
    output = ensure_extension(output)

    for img in images:
        im = Image.open(img)
        if im.mode == "RGBA":
            im = im.convert("RGB")
        pil_images.append(im)

    first = pil_images[0]
    rest = pil_images[1:]

    first.save(output, save_all=True, append_images=rest)
    rich.print(f"[green]Created PDF {output}[/green]")

# PDF to Images
@app.command()
def pdf2img(input: Annotated[str, typer.Argument(help="Input PDF file. Use quotes for path with spaces.")],
        output_folder: Annotated[str, typer.Option(
            ..., "-o", "--output", help="Output file location.",
            prompt="Output folder name"
            )] = "out_images"):
    
    """
    Convert each PDF page into a PNG. The page order determines the image order.\n
    Example:\n
    pdfcli file.pdf -o out_images 
    """

    Path(output_folder).mkdir(exist_ok=True) # TODO: Proper folder name verification
    pages = convert_from_path(input)

    for i, page in enumerate(pages):
        out_path = f"{output_folder}/page_{i+1}.png"
        page.save(out_path, "PNG")

    rich.print(f"[green]Images saved to ./{output_folder}/[/green]")

# Reorder PDF
@app.command()
def reorder(input: Annotated[str, typer.Argument(help="Input PDF file. Use quotes for path with spaces.")],
        output: Annotated[str, typer.Option(
            ..., "-o", "--output", help="Output PDF file (path + filename).",
            prompt="Output file name"
            )],
        order: Annotated[str, typer.Option(
            ..., "-r", "--order", help="Order of input files by their index",
            prompt="Pages order (e.g: 3,1,2)"
        )]):
    
    """
    Reorder PDF pages.\n
    Duplicates are ignored, only the first occurance is used. Pages not specified in the order will be appended at the end in their original sequence.
    Use "trim" instead if you want to keep only the specified pages.\n
    Example:\n
    pdfcli input.pdf -o output.pdf -r 3,1,2
    """

    reader = PdfReader(input)
    writer = PdfWriter()

    output = ensure_extension(output)
    page_order = dedupe_ordered([int(x)-1 for x in order.split(",")])
    total_pages = len(reader.pages)
    add_remaining_pages(page_order, total_pages)

    for page_number in range(total_pages):
        if page_number not in page_order:
            page_order.append(page_number)

    for idx in page_order:
        writer.add_page(reader.pages[idx])

    with open(output, "wb") as f:
        writer.write(f)
    rich.print(f"[green]Reordered and saved to {output}[/green]")

# Trim PDFs
@app.command()
def trim(input: Annotated[str, typer.Argument(help="Input PDF file. Use quotes for path with spaces.")],
        output: Annotated[str, typer.Option(
            ..., "-o", "--output", help="Output PDF file (path + filename).",
            prompt="Output file name"
            )],
        pages: Annotated[str, typer.Option(
            ..., "-p", "--page", help="Pages to keep. Please don't add any spaces. e.g. '1-5,7,10-12,9'",
            prompt="Pages (e.g. 1-5,7,10-12,9)"
        )]):
    
    """
    Trim or reorder pages of a PDF using page range syntax.\n
    Support ranges and specific pages such as "1-5" or "1,2,3". It can also reverse pages like "9-5", or "9, 6, 7", and reorder pages. Duplicates are allowed.\n
    Please specify without using spaces.\n
    Example:\n
        pdfcli output.pdf -i input.pdf -p 1-5,7,10-12,9
    """
    
    reader =  PdfReader(input)
    writer = PdfWriter()

    page_order = parse_page_ranges(pages)
    output = ensure_extension(output)
    
    for idx in page_order:
        writer.add_page(reader.pages[idx - 1])

    with open(output, "wb") as f:
        writer.write(f)
    rich.print(f"[green]Trimmed and saved to {output}[/green]")

if __name__ == "__main__":
    app()