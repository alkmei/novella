import os
from .metadata import load_metadata


def compile_story(story_path):
    metadata_path = os.path.join(story_path, "story.json")
    metadata = load_metadata(metadata_path)

    if "chapters" not in metadata or len(metadata["chapters"]) == 0:
        raise ValueError("No chapters found in metadata to compile.")

    output_path = os.path.join(story_path, metadata.title)

    with open(output_path, "w") as output_file:
        for chapter in metadata["chapters"]:
            chapter_filename = chapter.get("filename")
            chapter_path = os.path.join(story_path, chapter_filename)

            if not os.path.exists(chapter_path):
                raise FileNotFoundError(f"Chapter file not found: {chapter_path}")

            with open(chapter_path, "r") as chapter_file:
                # Write chapter content to the output file
                output_file.write(chapter_file.read())
                output_file.write("\n\n")  # Add space between chapters

    print(f"Story compiled successfully into {output_path}")
