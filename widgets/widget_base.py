from PyQt5.QtWidgets import QWidget, QFrame, QPushButton, QLabel
from PyQt5.QtCore import QSize, Qt

class QWidgetBase(QWidget):
    def __init__(self, parent=None, customX=500, customY=250):
        super().__init__(parent)

        if not hasattr(self, 'customX'):
            self.customX = customX
        if not hasattr(self, 'customY'):
            self.customY = customY

        self.setStyleSheet("background-color: #D3D3D3;")

        self.setFixedSize(QSize(self.customX, self.customY))
        self.setWindowTitle(self.icon_name)

        # Outer Frame setup
        outerFrame = QFrame(self)
        outerFrame.setGeometry(0, 0, self.customX, self.customY)  # Fills the parent widget
        outerFrame.setFrameShape(QFrame.Box)
        outerFrame.setLineWidth(2)
        outerFrame.setStyleSheet("QFrame { border: 2px solid black; }")

        # Top Frame setup
        topFrame = QFrame(outerFrame)
        topFrame.setGeometry(0, 0, self.customX, 30)
        topFrame.setStyleSheet("QFrame { background-color: #D3D3D3; }")

        # Label setup
        self.label = QLabel(self.icon_name, outerFrame)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # Aligns text to top-left
        self.label.setStyleSheet("QLabel { margin-left: 5px; color: black; font-weight: bold; background-color: #D3D3D3; border: none; }")
        # Position and size the label
        self.label.setGeometry(5, 5, 200, 20)  # Adjust size as needed

        # Close Button setup
        self.closeButton = QPushButton("X", self)  # Positioned relative to the main widget, not innerFrame
        self.closeButton.setFixedSize(60, 26)
        self.closeButton.setStyleSheet("QPushButton { border: none; background-color: #FFB6C1; font-weight: bold; }")
        self.closeButton.clicked.connect(self.closeWindow)
        # Position the close button in the top right corner of the main widget
        self.closeButton.move(self.width() - self.closeButton.width() - 2, 2)

    def closeWindow(self):
        print("closing window")
        self.close()
