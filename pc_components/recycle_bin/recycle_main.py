import common_vars as cv
from PyQt5.QtWidgets import QListWidget, QVBoxLayout
from ui_utils.draggable_widget import DraggableBase
from widgets.widget_base import QWidgetBase

class RecycleBinWindow(DraggableBase, QWidgetBase):
    def __init__(self, icon_name, parent=None):
        self.icon_name = icon_name
        super().__init__(parent)
        self.initUI()

    def initUI(self):

        self.deletedWidgetsList = QListWidget(self)
        for widget_info in cv.deleted_widgets:
            widget_name, delete_time = widget_info
            self.deletedWidgetsList.addItem(f"{widget_name} - Deleted at: {delete_time.strftime('%Y-%m-%d %H:%M:%S')}")

        layout = QVBoxLayout()
        layout.setContentsMargins(1, 30, 1, 1)
        layout.addWidget(self.deletedWidgetsList)
        self.setLayout(layout)
