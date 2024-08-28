import os
import pytest
from typer.testing import CliRunner
from pathlib import Path
from cli.__main__ import app  # Import the main CLI application

runner = CliRunner()


@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path


# Test for init command


def test_init_command(temp_dir):
    result = runner.invoke(
        app, ["init", "My New Story", "--author", "John Doe", str(temp_dir)]
    )

    assert result.exit_code == 0
    assert "Story 'My New Story' created successfully" in result.output

    metadata_path = temp_dir / "story.json"
    assert metadata_path.is_file()


# Test for init command with existing story


def test_init_command_existing_story(temp_dir):
    # First, create a story
    runner.invoke(app, ["init", "My New Story", "--author", "John Doe", str(temp_dir)])

    # Try creating another story in the same directory
    result = runner.invoke(
        app, ["init", "Another Story", "--author", "Jane Doe", str(temp_dir)]
    )

    assert result.exit_code != 0
    assert isinstance(result.exception, FileExistsError)


# Test for new (create chapter) command


def test_new_chapter_command(temp_dir):
    # First, create a story (so the metadata file exists)
    runner.invoke(app, ["init", "My New Story", "--author", "John Doe", str(temp_dir)])

    # Create a chapter
    result = runner.invoke(app, ["chapter", "new", "Chapter One", str(temp_dir)])

    assert result.exit_code == 0
    assert "Chapter 'Chapter One' created" in result.output

    chapter_path = temp_dir / "chapter_one.md"
    assert chapter_path.is_file()


# Test for new chapter command with existing chapter


def test_new_chapter_command_existing_chapter(temp_dir):
    # Create a story and a chapter
    runner.invoke(app, ["init", "My New Story", "--author", "John Doe", str(temp_dir)])
    runner.invoke(app, ["chapter", "new", "Chapter One", str(temp_dir)])

    # Try creating the same chapter again
    result = runner.invoke(app, ["chapter", "new", "Chapter One", str(temp_dir)])

    assert result.exit_code != 0
    assert isinstance(result.exception, FileExistsError)


# Test for compile command


def test_compile_command(temp_dir):
    # Create a story and a chapter
    runner.invoke(app, ["init", "My New Story", "--author", "John Doe", str(temp_dir)])
    runner.invoke(app, ["chapter", "new", "Chapter One", str(temp_dir)])

    # Compile the story
    result = runner.invoke(app, ["compile", str(temp_dir)])

    assert result.exit_code == 0
    assert "Story compiled successfully" in result.output

    output_path = temp_dir / "My New Story.md"
    assert output_path.is_file()


# Test for compile command with no chapters


def test_compile_command_no_chapters(temp_dir):
    # Create a story without chapters
    runner.invoke(app, ["init", "My New Story", "--author", "John Doe", str(temp_dir)])

    # Try to compile the story
    result = runner.invoke(app, ["compile", str(temp_dir)])

    assert result.exit_code != 0
    assert isinstance(result.exception, ValueError)
