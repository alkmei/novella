import pytest
import json
from novella.chapter import create_chapter, get_chapters, delete_chapter
from novella.story import Story


@pytest.fixture
def temp_directory(tmp_path):
    story = Story.new("Title")
    with open(tmp_path / "story.json", "w+") as f:
        f.write(story.model_dump_json(indent=4))

    return tmp_path


def test_create_chapter(temp_directory):
    path = temp_directory
    title = "New Chapter"

    # Call the function
    create_chapter(title, path)

    # Assertions
    chapter_path = path / "new_chapter.md"
    assert chapter_path.exists()
    with open(chapter_path, "r") as f:
        content = f.read()
    assert content == f"# {title}\n\n"

    # Check the story.json file
    with open(path / "story.json", "r") as f:
        story = json.load(f)
    assert len(story["chapters"]) == 1
    assert str(story["chapters"][0]) == str(chapter_path)


def test_get_chapters(temp_directory):
    path = temp_directory
    create_chapter("First Chapter", path)
    create_chapter("Second Chapter", path)

    chapters = get_chapters(path)

    assert len(chapters) == 2
    assert chapters[0] == path / "first_chapter.md"
    assert chapters[1] == path / "second_chapter.md"


def test_delete_chapter(temp_directory):
    path = temp_directory
    create_chapter("First Chapter", path)
    create_chapter("Second Chapter", path)

    delete_chapter(1, path)

    # Check the chapter file was deleted
    first_chapter_path = path / "first_chapter.md"
    assert not first_chapter_path.exists()

    # Check the story.json file
    with open(path / "story.json", "r") as f:
        story = json.load(f)
    assert len(story["chapters"]) == 1
    assert str(story["chapters"][0]) == str(path / "second_chapter.md")


def test_delete_chapter_no_chapters(temp_directory):
    path = temp_directory

    # Call and assert
    with pytest.raises(RuntimeError, match="There are no chapters to delete"):
        delete_chapter(1, path)


def test_delete_chapter_index_error(temp_directory):
    path = temp_directory
    create_chapter("Chapter", path)

    # Call and assert
    with pytest.raises(
        IndexError, match="Chapter number must be less than the number of chapters"
    ):
        delete_chapter(2, path)
