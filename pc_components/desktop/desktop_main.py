from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget
from PyQt5.QtCore import Qt

import common_vars as cv

from pc_components.desktop.desktop_utils.desktop_clicks import DesktopClicking
from pc_components.desktop.desktop_utils.desktop_icon_manager import DesktopIconManager

from pc_components.desktop.desktop_widgets.start_menu_widget import StartMenuWidget


class MainDesktop(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("uindou 94")

        # Calculate the position and size to place the window at the bottom
        desktop = QDesktopWidget()
        screenRect = desktop.availableGeometry()
        screenWidth = screenRect.width() - 600
        screenHeight = screenRect.height() - 300
        self.setGeometry(0, 0, screenWidth, screenHeight)
        self.setFixedSize(screenWidth, screenHeight)
        self.setStyleSheet('QTextEdit{background-image:url("' + cv.desktop_background +'");}')

        self.desktopIconManager = DesktopIconManager(self)
        self.desktopIconManager.add_icon(cv.recycle_bin_img, "rb")
        self.desktopIconManager.add_icon(cv.notes_img, "notes")
        # self.desktopIconManager.add_icon(cv.folder_img, "folder")
        self.desktopIconManager.add_icon(cv.web_browser_img, "web")
        self.desktopIconManager.add_icon(cv.music_img, "music")
        self.desktopIconManager.add_icon(cv.task_manager_img, "taskm")

        # self.startMenuWidget = StartMenuWidget(self)
        # self.startMenuHeight = 50  # Adjust as needed
        # self.startMenuWidget.setGeometry(0, screenHeight - self.startMenuHeight, screenWidth, self.startMenuHeight)
        # self.desktopClicking = DesktopClicking(self, self.desktopIconManager)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.RightButton:
            self.desktopClicking.right_clicking(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(cv.desktop_background)
        background = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio)
        painter.drawPixmap(self.rect(), background)


if __name__ == "__main__":
    app = QApplication([])
    mainWindow = MainDesktop()
    mainWindow.show()
    app.exec_()
