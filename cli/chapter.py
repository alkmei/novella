from pathlib import Path
from typing import Annotated, Optional

import typer
from novella import create_chapter

app = typer.Typer()


@app.command()
def new(
    title: str,
    path: Annotated[Optional[Path], typer.Argument()] = Path.cwd(),
):
    create_chapter(title, path)


if __name__ == "__main__":
    app()
