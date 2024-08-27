import json
import os
from pathlib import Path

import pytest
from novella import (
    create_chapter,
    get_chapters,
    compile_story,
    create_story,
    load_metadata,
    save_metadata,
)

# Helper functions for testing


@pytest.fixture
def mock_metadata():
    return {"title": "Test Story", "author": "Anonymous", "genres": [], "chapters": []}


@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path


# Tests for create_story


def test_create_story(temp_dir):
    create_story("My New Story", temp_dir, "John Doe")

    metadata_path = temp_dir / "story.json"
    assert metadata_path.is_file()

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    assert metadata["title"] == "My New Story"
    assert len(metadata["genres"]) == 0
    assert len(metadata["chapters"]) == 0
    assert metadata["author"] == "John Doe"


def test_create_story_existing_file(temp_dir):
    create_story("My New Story", temp_dir, "John Doe")

    with pytest.raises(FileExistsError):
        create_story("Another Story", temp_dir, "Jane Doe")


# Tests for create_chapter


def test_create_chapter(temp_dir, mock_metadata):
    save_metadata(mock_metadata, os.path.join(temp_dir, "story.json"))

    create_chapter("Chapter One", temp_dir)

    chapter_path = temp_dir / "chapter_one.md"
    assert chapter_path.is_file()

    with open(temp_dir / "story.json", "r") as f:
        metadata = json.load(f)

    assert len(metadata["chapters"]) == 1
    assert metadata["chapters"][0]["title"] == "Chapter One"
    assert metadata["chapters"][0]["filename"] == "chapter_one.md"


def test_create_chapter_file_exists(temp_dir, mock_metadata):
    save_metadata(mock_metadata, os.path.join(temp_dir, "story.json"))
    create_chapter("Chapter One", temp_dir)

    with pytest.raises(FileExistsError):
        create_chapter("Chapter One", temp_dir)


# Tests for get_chapters


def test_get_chapters(temp_dir, mock_metadata):
    mock_metadata["chapters"] = [{"title": "Chapter One", "filename": "chapter_one.md"}]
    save_metadata(mock_metadata, os.path.join(temp_dir, "story.json"))

    chapters = get_chapters(temp_dir)
    assert len(chapters) == 1
    assert chapters[0]["title"] == "Chapter One"


# Tests for compile_story


def test_compile_story(temp_dir, mock_metadata):
    mock_metadata["chapters"] = [{"title": "Chapter One", "filename": "chapter_one.md"}]
    save_metadata(mock_metadata, os.path.join(temp_dir, "story.json"))

    with open(temp_dir / "chapter_one.md", "w") as f:
        f.write("# Chapter One\n\nContent of chapter one.")

    compile_story(temp_dir)

    output_path = Path(os.path.join(temp_dir, "Test Story"))
    assert output_path.is_file()

    with open(output_path, "r") as f:
        content = f.read()

    assert "# Chapter One\n\nContent of chapter one." in content


def test_compile_story_no_chapters(temp_dir):
    save_metadata(
        {"title": "Test Story", "chapters": []}, os.path.join(temp_dir, "story.json")
    )

    with pytest.raises(ValueError):
        compile_story(temp_dir)


def test_compile_story_missing_chapter(temp_dir, mock_metadata):
    mock_metadata["chapters"] = [
        {"title": "Chapter One", "filename": "missing_chapter.md"}
    ]
    save_metadata(mock_metadata, os.path.join(temp_dir, "story.json"))

    with pytest.raises(FileNotFoundError):
        compile_story(temp_dir)
