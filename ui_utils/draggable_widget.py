from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import Qt, pyqtSignal, QRect, QSize
from pc_components.desktop.desktop_utils.desktop_clicks import DesktopIconClicking

class DraggableBase(QWidget):
    doubleClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.dragging = False
        self._mousePressPos = None
        self._mouseMovePos = None
        self.original_position = None
        self.file_path = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self._mousePressPos = event.globalPos()
            self._mouseMovePos = event.globalPos()
            self.original_position = self.pos()
        elif event.button() == Qt.RightButton:
            icon_clicking = DesktopIconClicking(self.parent(), self.desktopIconManager)
            icon_clicking.right_clicking(self, event)

    def mouseMoveEvent(self, event):
        if self.dragging:
            movePos = event.globalPos() - self._mouseMovePos
            self.move(self.pos() + movePos)
            self._mouseMovePos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

class DraggableQWidget(DraggableBase):
    pass

class DraggableQLabel(QLabel, DraggableBase):
    doubleClicked = pyqtSignal()

    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        DraggableBase.__init__(self, parent)
        self.icon_name_label = QLabel(self)
        self.icon_name = ""
        self.customFunction = None

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.check_overlap()

    def mouseDoubleClickEvent(self, event):
        print("Double clicked")
        self.doubleClicked.emit()

    def check_overlap(self):
        parent_bounds = self.parent().rect()
        current_icon_rect = QRect(self.pos(), QSize(self.width(), self.height()))

        if not parent_bounds.contains(current_icon_rect):
            print("Movement beyond screen borders detected. Moving back to original position.")
            self.move(self.original_position)
            return

        for sibling in self.parent().children():
            if isinstance(sibling, QWidget) and sibling is not self and sibling.isVisible():
                sibling_rect = QRect(sibling.pos(), QSize(sibling.width(), sibling.height()))
                # print(vars(sibling))
                if current_icon_rect.intersects(sibling_rect):
                    print(f"Overlap detected with {sibling}. Moving back to original position.")
                    self.move(self.original_position)
                    return

        self.original_position = self.pos()

    def set_icon_name(self, new_name):
        self.icon_name = new_name
        if hasattr(self, 'label'):
            self.label.setText(new_name)  # Update the label text
        else:
            print("Label attribute not found.")


def check_if_folder():
    pass


