import json
import os

import pytest

from novella import create_story
from novella.story import Story


@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path


@pytest.fixture
def mock_story():
    return Story(title="Test Story", author="John Doe", chapters=[])


def test_create_story(temp_dir, mock_story):
    create_story("Test Story", temp_dir, "John Doe")

    story_path = os.path.join(temp_dir, "story.json")
    assert os.path.exists(story_path)

    with open(story_path, "r") as f:
        story_json = json.load(f)
        story = Story(**story_json)
        assert story == mock_story


def test_create_story_already_exists(temp_dir, mock_story):
    create_story("Test Story", temp_dir, "John Doe")

    with pytest.raises(FileExistsError):
        create_story("Another Story", temp_dir, "Jane Doe")


def test_story_anonymous(temp_dir):
    create_story("Test Story", temp_dir)
    story_path = os.path.join(temp_dir, "story.json")

    with open(story_path, "r") as f:
        story_json = json.load(f)
        story = Story(**story_json)
        assert story.author == "Anonymous"
