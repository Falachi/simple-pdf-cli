# Simple PDF-CLI

Simple PDF-CLI is a simple CLI app to edit PDFs directly from the terminal. Current features:

- Merge multiple PDFs
- Convert PDF to images
- Combine images to a PDF
- Reorder pages of a PDF
- Trim pages of a PDF
- Split a PDF into multiple PDFs
- Encrypt a PDF
- Decrypt a PDF

## Usage Examples

**Merge**

```bash
pdfcli merge file1.pdf file2.pdf -o merged.pdf
```

**Images to PDF**

```bash
pdfcli image1.png image2.png image3.png -o output.pdf
```

**PDF to Images**

```bash
pdfcli file.pdf -o out_images
```

**Reorder**

```bash
pdfcli input.pdf -o output.pdf -r 3,1,2
```

**Trim**

```bash
pdfcli input.pdf -o output.pdf -p 1-5,7,10-12,9
```

**Split**

```bash
pdfcli split input.pdf -o out_pdfs -p 1-5,3-6,7
```

**Encrypt**

```bash
pdfcli encrypt file.pdf -o output.pdf -p password1
```

**Decrypt**

```bash
pdfcli decrypt file.pdf -o output.pdf -p password1
```

## Installation

**Using pip (recommended):**

```bash
pip install simple-pdf-cli
```

**Manual Installation**

1. Clone the repo

```bash
git clone https://github.com/Falachi/simple-pdf-cli.git
```

2. Go to project directory

```bash
cd simple-pdf-cli
```

3. Install package

```bash
pip install -e .
```

## To-Do List

- [x] Implement proper type and error checking
- [ ] Compress PDF
- [x] Split PDF
- [x] Password protect
- [ ] Allow a `.txt` file as input for arguments that accept multiple files
- [ ] Edit PDF metadata
- [ ] Upload to PyPI
- [ ] Create a GUI version
- Etc.
