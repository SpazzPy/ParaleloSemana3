from PyQt5.QtWidgets import QWidget, QMenu, QAction, QPushButton
from PyQt5.QtCore import QPoint

from PyQt5.QtWidgets import QVBoxLayout

class StartMenuWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        # Start Menu Button
        self.startMenuButton = QPushButton("Start", self)
        self.startMenuButton.clicked.connect(self.showStartMenu)
        self.layout.addWidget(self.startMenuButton)

        # Create the menu
        self.startMenu = QMenu(self)

        # Add actions
        action1 = QAction("Application 1", self)
        action1.triggered.connect(lambda: self.launchApplication("Application 1"))
        self.startMenu.addAction(action1)

        action2 = QAction("Application 2", self)
        action2.triggered.connect(lambda: self.launchApplication("Application 2"))
        self.startMenu.addAction(action2)

        self.setLayout(self.layout)

    def showStartMenu(self):
        menuPos = self.startMenuButton.mapToGlobal(QPoint(0, 0))
        menuPos.setY(menuPos.y() - self.startMenu.sizeHint().height())
        self.startMenu.exec_(menuPos)
