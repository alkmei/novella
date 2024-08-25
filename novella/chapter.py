import os
from novella.metadata import load_metadata, save_metadata


def create_chapter(title, story_path):
    metadata_path = os.path.join(story_path, "story.json")
    metadata = load_metadata(metadata_path)

    if "chapters" not in metadata:
        metadata["chapters"] = []

    chapter_filename = f"{title.replace(' ', '_').lower()}.md"
    chapter_path = os.path.join(story_path, chapter_filename)

    if os.path.exists(chapter_path):
        raise FileExistsError(f"Chapter file already exists: {chapter_path}")

    with open(chapter_path, "w") as chapter_file:
        chapter_file.write(f"# {title}\n\n")

    metadata["chapters"].append({"title": title, "filename": chapter_filename})

    save_metadata(metadata, metadata_path)

    print(f"Chapter '{title}' created at {chapter_path} and metadata updated.")


def list_chapters():
    # Logic to list all chapters
    pass
