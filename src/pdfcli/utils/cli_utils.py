from rich.console import Console

console = Console()

def rprint(message: str,*, status: int | None = None) -> None:

  styles = {
    0: "green",
    1: "red"
  }

  console.print(message, style=styles[status])