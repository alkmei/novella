from typing_extensions import Annotated
from pathlib import Path
from typing import Optional
import typer
from novella import create_story

app = typer.Typer()


@app.command()
def init(
    title: str,
    author: str = "Anonymous",
    path: Annotated[Optional[Path], typer.Argument()] = Path.cwd(),
):
    create_story(title, path, author)


if __name__ == "__main__":
    app()
