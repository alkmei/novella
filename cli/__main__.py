import typer
import cli.chapter as chapter
import cli.init as init
import cli.compile as compile

app = typer.Typer()

app.command(help="Initializes a story")(init.init)
app.command(help="Compiles a story")(compile.compile)
app.add_typer(chapter.app, name="chapter", help="Handles chapters")


if __name__ == "__main__":
    app()
