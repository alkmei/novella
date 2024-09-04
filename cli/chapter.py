from pathlib import Path
from typing import Annotated, Optional

import typer
from novella import create_chapter, get_chapters
from rich.console import Console
from rich.table import Table

app = typer.Typer()

console = Console()


@app.command()
def new(
    title: str,
    path: Annotated[Optional[Path], typer.Argument()] = Path.cwd(),
):
    create_chapter(title, path)


@app.command()
def ls(path: Annotated[Optional[Path], typer.Argument()] = Path.cwd()):
    chapters = get_chapters(path)
    table = Table("#", "Name")
    for i, chapter in enumerate(chapters):
        table.add_row((i + 1).__str__(), chapter.name)

    console.print(table)


if __name__ == "__main__":
    app()
