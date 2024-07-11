import pytest
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from novella.story import (
    Story,
    create_new_story,
    load_story,
)  # Replace 'your_module' with the actual module name


def test_create_new_story():
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        create_new_story("Test Title", "Test Author", temp_path)

        # Check if the file was created
        story_file = temp_path / "story.json"
        assert story_file.exists()

        # Check if the content is correct
        with story_file.open("r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            assert data["title"] == "Test Title"
            assert data["author"] == "Test Author"
            assert data["chapters"] == []


def test_load_story():
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        story_file = temp_path / "story.json"

        # Create a story file
        create_new_story("Test Title", "Test Author", temp_path)

        # Load the story
        loaded_story = load_story(story_file)

        # Check if the loaded story has the correct attributes
        assert loaded_story.title == "Test Title"
        assert loaded_story.author == "Test Author"
        assert loaded_story.chapters == []


def test_create_and_load_story_with_chapters():
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        story_file = temp_path / "story.json"

        # Create a story with chapters
        story = Story(
            "Test Title", "Test Author", [Path("Chapter1.md"), Path("Chapter2.md")]
        )
        with story_file.open("w", encoding="utf-8") as json_file:
            json.dump(story.__dict__(), json_file, indent=4)

        # Load the story
        loaded_story = load_story(story_file)

        # Check if the loaded story has the correct attributes
        assert loaded_story.title == "Test Title"
        assert loaded_story.author == "Test Author"
        assert loaded_story.chapters == [Path("Chapter1.md"), Path("Chapter2.md")]


if __name__ == "__main__":
    pytest.main()
