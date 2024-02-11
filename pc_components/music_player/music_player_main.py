from PyQt5.QtWidgets import QFormLayout, QWidget, QVBoxLayout, QPushButton, QFrame
from pyqt_find_path_widget import FindPathWidget
from pyqt_music_player_widget import MusicPlayerWidget

from ui_utils.draggable_widget import DraggableBase
from widgets.widget_base import QWidgetBase

class MusicPlayerWindow(DraggableBase, QWidgetBase):
    def __init__(self, icon_name, parent=None):
        self.icon_name = icon_name
        super().__init__(parent)

        self.setStyleSheet("background-color: white;")

        self.__findPathWidget = FindPathWidget()
        self.__findPathWidget.setExtOfFiles('Audio Files (*.mp3)')
        self.__findPathWidget.added.connect(self.__added)

        lay = QFormLayout()
        lay.addRow('Audio File', self.__findPathWidget)
        lay.setContentsMargins(0, 60, 0, 0)

        pathFindWidget = QWidget()
        pathFindWidget.setLayout(lay)

        self.__musicPlayerWidget = MusicPlayerWidget()

        lay = QVBoxLayout()
        lay.addWidget(pathFindWidget)
        lay.addWidget(self.__musicPlayerWidget)
        lay.setContentsMargins(3, 30, 3, 3)

        self.setLayout(lay)

        # duplicate this to get it to close
        self.closeButton.deleteLater()
        self.closeButton = QPushButton("X", self)  # Positioned relative to the main widget, not innerFrame
        self.closeButton.setFixedSize(60, 26)
        self.closeButton.setStyleSheet("QPushButton { border: none; background-color: #FFB6C1; font-weight: bold; }")
        self.closeButton.clicked.connect(self.closeWindow)
        # Position the close button in the top right corner of the main widget
        self.closeButton.move(self.width() - self.closeButton.width() - 2, 2)

    def __added(self, filename: str):
        self.__musicPlayerWidget.setMedia(filename)

