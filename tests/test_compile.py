import pytest
from novella.compile import compile_story
from novella.story import Story  # Adjust import based on your actual module


def test_compile_story_success(tmp_path):
    # Setup
    story = Story(
        title="My Story",
        author="Author Name",
        chapters=[tmp_path / "chapter1.md", tmp_path / "chapter2.md"],
    )

    # Save story.json
    with open(tmp_path / "story.json", "w") as f:
        f.write(story.model_dump_json())

    # Create chapter files
    with open(tmp_path / "chapter1.md", "w") as f:
        f.write("Content of chapter 1")
    with open(tmp_path / "chapter2.md", "w") as f:
        f.write("Content of chapter 2")

    output_file_path = tmp_path / "My Story.md"

    # Call the function
    compile_story(tmp_path)

    # Assertions
    assert output_file_path.exists()
    with open(output_file_path, "r") as output_file:
        content = output_file.read()
    expected_content = "Content of chapter 1\n\nContent of chapter 2\n\n"
    assert content == expected_content


def test_compile_story_no_chapters(tmp_path):
    # Setup
    story = Story(title="My Story", author="Author Name", chapters=[])

    # Save story.json
    with open(tmp_path / "story.json", "w") as f:
        f.write(story.json())

    # Call and assert
    with pytest.raises(ValueError, match="No chapters found in metadata to compile."):
        compile_story(tmp_path)


def test_compile_story_missing_chapter(tmp_path):
    # Setup
    story = Story(
        title="My Story",
        author="Author Name",
        chapters=[tmp_path / "chapter1.md", tmp_path / "chapter2.md"],
    )

    # Save story.json
    with open(tmp_path / "story.json", "w") as f:
        f.write(story.json())

    # Create only one chapter file
    with open(tmp_path / "chapter1.md", "w") as f:
        f.write("Content of chapter 1")

    # Call and assert
    with pytest.raises(FileNotFoundError, match="Chapter file not found:"):
        compile_story(tmp_path)
