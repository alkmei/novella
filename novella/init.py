import os
from pathlib import Path
from novella.story import Story, save_story


def create_story(title: str, path: Path, author: str = "Anonymous"):
    if Path(os.path.join(path, "story.json")).is_file():
        raise FileExistsError()

    if not os.path.exists(path):
        os.makedirs(path)

    story = Story.new(title, author)
    story_file = os.path.join(path, "story.json")

    save_story(story, story_file)

    print(f"Story '{title}' created successfully at {path}")
