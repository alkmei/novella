import os
import json
from pathlib import Path
from typing import List

from pydantic import BaseModel, Field, ValidationError


class Story(BaseModel):
    title: str
    author: str = Field(default="Anonymous")
    chapters: List[Path] = Field(default_factory=list)

    @staticmethod
    def new(title: str, author: str = "Anonymous"):
        return Story(title=title, author=author, chapters=[])


def load_story(story_path: str) -> Story:
    if not os.path.exists(story_path):
        raise FileNotFoundError(f"Story file not found: {story_path}")

    with open(story_path, "r") as file:
        story_data = json.load(file)

    if "chapters" in story_data:
        story_data["chapters"] = [Path(chapter) for chapter in story_data["chapters"]]
    try:
        Story.model_validate(story_data)
    except ValidationError as e:
        raise ValueError(f"Invalid story data: {e}")

    story = Story(**story_data)

    return story


def save_story(story: Story, story_path: str):
    story_json_str = story.model_dump_json(indent=4)

    with open(story_path, "w") as file:
        file.write(story_json_str)
