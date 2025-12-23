from rich.console import Console
from pathlib import Path

console = Console()

def rprint(message: str,*, status: int | None = None) -> None:

  styles = {
    0: "green",
    1: "red"
  }

  if status is None:
    console.print(message)
    return

  console.print(message, style=styles[status])


# Read all PDF files from a text file
def read_pdf_list(file_path: str) -> list[str]:

  pdfs = []
  try:
    with open(file_path, "r") as f:
      for line in f:
        line = line.strip()
        if line and line.lower().endswith(".pdf"):
          pdfs.append(line)
  except Exception as e:
    rprint(f"Failed to read PDF list from {file_path}: {e}", status=1)
    return []
  
  return pdfs

def get_all_pdfs_in_folder(folder_path: str) -> list[str]:

  path = Path(folder_path)
  if not path.is_dir():
    rprint(f"{folder_path} is not a valid directory.", status=1)
    return []
  
  pdfs = [str(file) for file in path.glob("*.pdf") if file.is_file()]
  if not pdfs:
    rprint(f"No PDF files found in {folder_path}.", status=1)

  pdfs.sort()
  
  rprint(f"Found {len(pdfs)} PDF files in {folder_path}.", status=None)

  return pdfs