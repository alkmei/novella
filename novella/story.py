from pathlib import Path
import json


class Story:
    title: str
    author: str
    chapters: list[Path]

    def __init__(self, title: str, author: str, chapters: list[Path] = []) -> None:
        self.title = title
        self.author = author
        self.chapters = chapters


def create_new_story(title: str, author: str, path: Path = Path(".")):
    story = Story(title, author, [Path("README.md")])
    file_path = path / "story.json"
    with file_path.open("w", encoding="utf-8") as json_file:
        json.dump(vars(story), json_file, indent=4)


def load_story(story: Path) -> Story:
    with story.open("r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return Story(
        title=data["title"],
        author=data["author"],
        chapters=[Path(chapter) for chapter in data.get("chapters", [])],
    )

