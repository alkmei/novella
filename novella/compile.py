import os
from pathlib import Path

from .story import load_story


def compile_story(path: Path):
    story_path = os.path.join(path, "story.json")
    story = load_story(story_path)

    if len(story.chapters) == 0:
        raise ValueError("No chapters found in metadata to compile.")

    output_path = os.path.join(path, story.title + ".md")

    with open(output_path, "w") as output_file:
        for chapter_path in story.chapters:
            chapter_path = path / chapter_path
            if not os.path.isfile(chapter_path):
                raise FileNotFoundError(f"Chapter file not found: {chapter_path}")

            with open(chapter_path, "r") as chapter_file:
                output_file.write(chapter_file.read())
                output_file.write("\n\n")

    print(f"Story compiled successfully into {output_path}")
