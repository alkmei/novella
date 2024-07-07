from pathlib import Path
import json


class Story:
    title: str
    author: str

    def __init__(self, title: str, author: str) -> None:
        self.title = title
        self.author = author


def create_new_story(title: str, author: str, path: Path):
    story = Story(title, author)
    with path.open("w", encoding="utf-8") as json_file:
        json.dump(vars(story), json_file, indent=4)
