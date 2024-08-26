from typing_extensions import Annotated
from pathlib import Path
from typing import Optional
import typer
from novella import compile_story

app = typer.Typer()


@app.command()
def compile(
    path: Annotated[Optional[Path], typer.Argument()] = Path.cwd(),
):
    compile_story(path)


if __name__ == "__main__":
    app()
