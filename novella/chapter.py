import os
from pathlib import Path

import send2trash

from .story import load_story, save_story


def create_chapter(title: str, path: Path):
    story_path = os.path.join(path, "story.json")
    story = load_story(story_path)

    chapter_filename = f"{title.replace(' ', '_').lower()}.md"
    chapter_path = os.path.join(path, chapter_filename)

    if os.path.exists(chapter_path):
        raise FileExistsError(f"Chapter file already exists: {chapter_path}")

    with open(chapter_path, "w") as chapter_file:
        chapter_file.write(f"# {title}\n\n")

    story.chapters.append(Path(chapter_path))

    save_story(story, story_path)

    print(f"Chapter '{title}' created at {chapter_path} and metadata updated.")


def get_chapters(path: Path):
    story_path = os.path.join(path, "story.json")
    story = load_story(story_path)

    return story.chapters


def delete_chapter(number: int, path: Path):
    if number < 1:
        raise IndexError("Chapter number must be positive")
    story_path = os.path.join(path, "story.json")
    story = load_story(story_path)

    if len(story.chapters) == 0:
        raise RuntimeError("There are no chapters to delete")

    if len(story.chapters) < number:
        raise IndexError("Chapter number must be less than the number of chapters")

    send2trash.send2trash(story.chapters[number - 1])
    story.chapters.pop(number - 1)

    save_story(story, story_path)

    print(f"Chapter '{number}' deleted.")
