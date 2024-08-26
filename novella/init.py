import os
import json
from pathlib import Path


def create_story(title: str, path: Path, author: str | None = None):
    if not os.path.exists(path):
        os.makedirs(path)

    metadata = {
        "title": title,
        "author": author if author else "Anonymous",
        "genres": [],
        "chapters": [],
    }

    metadata_file = os.path.join(path, "story.json")

    with open(metadata_file, "w+") as file:
        json.dump(metadata, file, indent=4)

    print(f"Story '{title}' created successfully at {path}")
