# Simple PDF-CLI

Simple PDF-CLI is a simple CLI app to edit PDFs directly from the terminal. Current features:

- Merge multiple PDFs
- Convert PDF to images
- Combine images to a PDF
- Reorder pages of a PDF
- Trim pages of a PDF

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
pdfcli output.pdf -i input.pdf -p 1-5,7,10-12,9
```

## To-Do List

- [ ] Upload to PyPI
- [ ] Compress PDF
- [ ] Split PDF
- [ ] Password protect
- [ ] Allow a `.txt` file as input for arguments that accept multiple files
- [ ] Edit PDF metadata
- [ ] Create a GUI version
- Etc.
