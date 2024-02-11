import os
import uuid

from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from pc_components.music_player.music_player_main import MusicPlayerWindow
from pc_components.task_manager.task_manager_main import TaskManagerWindow
from pc_components.web_navigation.web_nav_main import WebBrowserWindow
from ui_utils.draggable_widget import DraggableQLabel
from pc_components.folder_component.folder_main import FolderWindow
from pc_components.text_editor.text_editor_main import NotesWindow
from pc_components.recycle_bin.recycle_main import RecycleBinWindow

import common_vars as cv

class DesktopIconManager:
    def __init__(self, parent):
        self.parent = parent
        self.icons = []
        self.icon_width = 50
        self.icon_height = 50
        self.margin = 0
        self.icon_paths = {}

    def add_icon(self, icon_path, icon_type, mouse_pos=None):
        icon_id = str(uuid.uuid4())
        file_path = self.icon_paths.get(icon_id, None)

        if icon_type == "notes" and not file_path:
            file_path = self.generate_new_file_path()
            self.icon_paths[icon_id] = file_path

        if mouse_pos is not None and self.is_position_valid(mouse_pos):
            x, y = mouse_pos.x(), mouse_pos.y()
        else:
            x, y = self.find_next_available_position()

        icon = DraggableQLabel(self.parent)
        icon.desktopIconManager = self
        pixmap = QPixmap(icon_path)
        icon.setPixmap(pixmap.scaled(self.icon_width, self.icon_height))
        icon.move(x, y)
        icon.setFixedSize(self.icon_width, self.icon_height + 40)

        icon_name = "No Name"
        customFunction = None
        if icon_type == "rb":
            icon_name = cv.recycle_name
            customFunction = self.open_recycle_bin
        elif icon_type == "notes":
            icon_name = cv.notes_name
            customFunction = self.open_notes
        elif icon_type == "folder":
            icon_name = cv.folder_name
            customFunction = self.open_folder
        elif icon_type == "web":
            icon_name = cv.web_browser_name
            customFunction = self.open_browser
        elif icon_type == "music":
            icon_name = cv.music_name
            customFunction = self.open_music
        elif icon_type == "taskm":
            icon_name = cv.task_manager_name
            customFunction = self.open_task

        if customFunction is not None:
            if icon_type == "notes":
                icon.doubleClicked.connect(lambda: customFunction(icon_name, icon_id))
            else:
                icon.doubleClicked.connect(lambda: customFunction(icon_name))
            icon.customFunction = customFunction

        # Label setup
        icon.label = QLabel(icon_name, icon)
        icon.label.setAlignment(Qt.AlignCenter)
        icon.label.setStyleSheet("QLabel { color: black; font-weight: bold; border: none; }")
        icon.label.setGeometry(0, self.icon_height + 20, self.icon_width, 20)

        icon.show()

        self.icons.append(icon)

    def remove_icon(self, icon):
        if icon in self.icons:
            self.icons.remove(icon)
            icon.deleteLater()

    def is_position_empty(self, pos):
        new_icon_rect = QRect(pos, QSize(self.icon_width, self.icon_height))
        for icon in self.icons:
            if icon.geometry().intersects(new_icon_rect):
                return False
        return True

    def is_position_valid(self, pos):
        parent_rect = QRect(0, 0, self.parent.width(), self.parent.height())
        icon_rect = QRect(pos.x(), pos.y(), self.icon_width, self.icon_height)
        return parent_rect.contains(icon_rect) and self.is_position_empty(pos)

    def find_next_available_position(self):
        x, y = 0, 0
        while True:
            pos = QPoint(x, y)
            if self.is_position_valid(pos) and self.is_position_empty(pos):
                return x, y

            x += self.icon_width + self.margin
            if x + self.icon_width > self.parent.width():
                x = 0
                y += self.icon_height + self.margin
            if y + self.icon_height > self.parent.height():
                print("No more space available for icons.")
                return

    def generate_new_file_path(self):
        new_file_name = str(uuid.uuid4()) + ".txt"
        return os.path.join(cv.notes_path, new_file_name)

    def open_recycle_bin(self, icon_name):
        self.qWindow = RecycleBinWindow(icon_name, self.parent)
        self.qWindow.show()

    def open_notes(self, icon_name, icon_id):
        file_path = self.icon_paths.get(icon_id, None)
        self.qWindow = NotesWindow(icon_id, icon_name, file_path, self.parent)
        self.qWindow.show()

    def open_folder(self, icon_name):
        self.qWindow = FolderWindow(icon_name, self.parent)
        self.qWindow.show()

    def open_browser(self, icon_name):
        self.qWindow = WebBrowserWindow(icon_name, self.parent)
        self.qWindow.show()

    def open_music(self, icon_name):
        self.qWindow = MusicPlayerWindow(icon_name, self.parent)
        self.qWindow.show()

    def open_task(self, icon_name):
        self.qWindow = TaskManagerWindow(icon_name, self.parent)
        self.qWindow.show()
