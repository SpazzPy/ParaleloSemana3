import uuid, os
import common_vars as cv
from PyQt5.QtWidgets import QPlainTextEdit
from ui_utils.draggable_widget import DraggableBase
from widgets.widget_base import QWidgetBase

class NotesWindow(DraggableBase, QWidgetBase):
    def __init__(self, icon_id, icon_name, filePath=None, parent=None):
        self.icon_name = icon_name
        super().__init__(parent)
        self.icon_id = icon_id
        self.filePath = filePath if filePath else self.generate_new_file_name()

        self.initUI()

    def initUI(self):
        self.tEditor = QPlainTextEdit(self)
        self.loadText()
        self.tEditor.move(16, 44)
        self.tEditor.resize(468, 189)
        self.tEditor.setStyleSheet("QPlainTextEdit {background-color: white;}")
        self.tEditor.textChanged.connect(self.saveText)

    def generate_new_file_name(self):
        new_file_name = str(uuid.uuid4()) + ".txt"
        return os.path.join(cv.notes_path, new_file_name)

    def saveText(self):
        text = self.tEditor.toPlainText()
        with open(self.filePath, 'w') as file:
            file.write(text)

    def loadText(self):
        try:
            with open(self.filePath, 'r') as file:
                self.tEditor.setPlainText(file.read())
        except FileNotFoundError:
            self.saveText()

