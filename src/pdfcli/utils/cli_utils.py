
import rich

def rprint(message: str,*, status: int | None = None) -> None:

  styles = {
    0: "green",
    1: "red"
  }

  rich.print(message, styles=styles.get(status, None))