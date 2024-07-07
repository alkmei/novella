import json
import pytest
from pathlib import Path
from novella.story import create_new_story


@pytest.fixture
def temp_json_file(tmp_path):
    """Fixture to provide a temporary JSON file path."""
    return tmp_path / "temp_story.json"


def test_create_new_story(temp_json_file):
    # Define test input
    title = "Test Title"
    author = "Test Author"

    # Call the function to test
    create_new_story(title, author, temp_json_file)

    # Check if the file was created
    assert temp_json_file.exists()

    # Read the JSON content from the file
    with temp_json_file.open("r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    # Assert the content is correct
    assert data["title"] == title
    assert data["author"] == author
