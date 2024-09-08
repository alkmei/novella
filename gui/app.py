import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QLabel,
    QListWidget,
    QMessageBox,
    QInputDialog,
)
from PySide6.QtCore import Qt
from novella.init import create_story
from novella.chapter import create_chapter, get_chapters, delete_chapter
from novella.compile import compile_story


class StoryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Story Editor")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Story creation
        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Enter story title")
        layout.addWidget(self.title_input)

        self.author_input = QLineEdit(self)
        self.author_input.setPlaceholderText("Enter author name (optional)")
        layout.addWidget(self.author_input)

        self.path_input = QLineEdit(self)
        self.path_input.setPlaceholderText("Select story directory")
        layout.addWidget(self.path_input)

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_folder)
        layout.addWidget(self.browse_button)

        self.create_story_button = QPushButton("Create Story", self)
        self.create_story_button.clicked.connect(self.create_story)
        layout.addWidget(self.create_story_button)

        # Chapter management
        self.chapter_list = QListWidget(self)
        layout.addWidget(self.chapter_list)

        self.add_chapter_button = QPushButton("Add Chapter", self)
        self.add_chapter_button.clicked.connect(self.add_chapter)
        layout.addWidget(self.add_chapter_button)

        self.delete_chapter_button = QPushButton("Delete Chapter", self)
        self.delete_chapter_button.clicked.connect(self.delete_chapter)
        layout.addWidget(self.delete_chapter_button)

        # Compile story
        self.compile_button = QPushButton("Compile Story", self)
        self.compile_button.clicked.connect(self.compile_story)
        layout.addWidget(self.compile_button)

        self.setLayout(layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder:
            self.path_input.setText(folder)

    def create_story(self):
        title = self.title_input.text()
        author = self.author_input.text()
        path = self.path_input.text()

        if not title or not path:
            QMessageBox.warning(
                self, "Input Error", "Please provide both title and directory."
            )
            return

        try:
            create_story(title, Path(path), author)
            QMessageBox.information(self, "Success", "Story created successfully!")
            self.update_chapter_list()
        except FileExistsError:
            QMessageBox.critical(
                self, "Error", "Story already exists in the selected directory."
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def update_chapter_list(self):
        path = self.path_input.text()
        try:
            chapters = get_chapters(Path(path))
            self.chapter_list.clear()
            for chapter in chapters:
                self.chapter_list.addItem(str(chapter))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def add_chapter(self):
        path = self.path_input.text()
        if not path:
            QMessageBox.warning(self, "Input Error", "Please select a story directory.")
            return

        title, ok = QInputDialog.getText(self, "Add Chapter", "Enter chapter title:")
        if ok and title:
            try:
                create_chapter(title, Path(path))
                self.update_chapter_list()
            except FileExistsError:
                QMessageBox.critical(self, "Error", "Chapter file already exists.")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def delete_chapter(self):
        path = self.path_input.text()
        if not path:
            QMessageBox.warning(self, "Input Error", "Please select a story directory.")
            return

        selected_chapter = self.chapter_list.currentRow()
        if selected_chapter < 0:
            QMessageBox.warning(
                self, "Input Error", "Please select a chapter to delete."
            )
            return

        try:
            delete_chapter(selected_chapter + 1, Path(path))
            self.update_chapter_list()
        except IndexError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def compile_story(self):
        path = self.path_input.text()
        if not path:
            QMessageBox.warning(self, "Input Error", "Please select a story directory.")
            return

        try:
            compile_story(Path(path))
            QMessageBox.information(self, "Success", "Story compiled successfully!")
        except FileNotFoundError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
