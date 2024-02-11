from PyQt5.QtWidgets import QVBoxLayout

from ui_utils.draggable_widget import DraggableBase
from widgets.widget_base import QWidgetBase

class FolderWindow(DraggableBase, QWidgetBase):
    def __init__(self, icon_name, parent=None):
        self.icon_name = icon_name
        super().__init__(parent)
        self.initUI()

    def initUI(self):

        layout = QVBoxLayout()
        layout.setContentsMargins(1, 30, 1, 1)
