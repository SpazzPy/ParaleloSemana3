
from PyQt5.QtWidgets import QWidget, QMenu, QMessageBox, QInputDialog
from PyQt5.QtGui import QCursor
from datetime import datetime
import common_vars as cv

class DesktopClicking(QWidget):
    def __init__(self, parent=None, desktopIconManager=None):
        super().__init__(parent)
        self.desktopIconManager = desktopIconManager

    def right_clicking(self, event):
        contextMenu = QMenu(self)
        mouse_pos = self.mapFromGlobal(QCursor.pos())

        action1 = contextMenu.addAction("New: Folder")
        action2 = contextMenu.addAction("New: Notes")
        action3 = contextMenu.addAction("New: Recycle Bin")
        action4 = contextMenu.addAction("New: Browser")
        action5 = contextMenu.addAction("New: Music Player")
        action6 = contextMenu.addAction("New: Task Manager")

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        if action == action1:
            self.desktopIconManager.add_icon(cv.folder_img, "folder", mouse_pos)
        elif action == action2:
            self.desktopIconManager.add_icon(cv.notes_img, "notes", mouse_pos)
        elif action == action3:
            self.desktopIconManager.add_icon(cv.recycle_bin_img, "rb", mouse_pos)
        elif action == action4:
            self.desktopIconManager.add_icon(cv.web_browser_img, "web", mouse_pos)
        elif action == action5:
            self.desktopIconManager.add_icon(cv.music_img, "music", mouse_pos)
        elif action == action6:
            self.desktopIconManager.add_icon(cv.task_manager_img, "taskm", mouse_pos)


class DesktopIconClicking(QWidget):
    def __init__(self, parent=None, desktopIconManager=None):
        super().__init__(parent)
        self.desktopIconManager = desktopIconManager

    def right_clicking(self, widget, event):
        contextMenu = QMenu(self)

        action1 = contextMenu.addAction("Rename")
        action2 = contextMenu.addAction("Delete")

        action = contextMenu.exec_(QCursor.pos())

        if action == action1:
            new_name, ok = QInputDialog.getText(self, 'Rename Icon', 'Enter new name:')
            if ok:
                widget.set_icon_name(new_name)
        elif action == action2:
            reply = QMessageBox.question(self, 'Delete Icon', 'Are you sure you want to delete this icon?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            # print(vars(widget))
            # print(widget.customFunction)
            if reply == QMessageBox.Yes:
                rlabel = "Widget name not found"
                try:
                    label1 = str(widget.icon_name_label.text()).strip()
                    if label1 != "":
                        rlabel = label1
                    else:
                        label2 = str(widget.label.text()).strip()
                        rlabel = label2
                except Exception as e:
                    pass

                cv.deleted_widgets.append([rlabel, datetime.now()])
                self.desktopIconManager.remove_icon(widget)
