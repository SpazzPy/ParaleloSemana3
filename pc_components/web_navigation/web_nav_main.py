from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QVBoxLayout, QToolBar, QAction, QLineEdit, QFrame, QHBoxLayout, QPushButton, QLabel

from PyQt5.QtWebEngineWidgets import QWebEngineView
from ui_utils.draggable_widget import DraggableBase
from widgets.widget_base import QWidgetBase


class WebBrowserWindow(DraggableBase, QWidgetBase):
	def __init__(self, icon_name, parent=None, customX=1200, customY=600):
		self.customX = customX
		self.customY = customY
		self.icon_name = icon_name
		super().__init__(parent)

		self.homeUrl = "http://www.google.com"

		self.layout = QVBoxLayout(self)
		self.layout.setContentsMargins(5, 30, 5, 10)

		# Toolbar Frame
		self.toolbarFrame = QFrame(self)
		self.toolbarFrameLayout = QHBoxLayout(self.toolbarFrame)
		self.toolbarFrameLayout.setContentsMargins(12, 0, 12, 0)

		# Navigation Toolbar
		self.navtb = QToolBar("Navigation")
		self.toolbarFrameLayout.addWidget(self.navtb)

		# Adding the toolbar frame to the main layout
		self.layout.addWidget(self.toolbarFrame)

		# Browser Frame
		self.browserFrame = QFrame(self)
		self.browserFrameLayout = QVBoxLayout(self.browserFrame)
		self.browserFrameLayout.setContentsMargins(16, 0, 16, 16)
		self.browserFrameLayout.setSpacing(0)

		# Browser setup
		self.browser = QWebEngineView()
		self.browser.setUrl(QUrl(self.homeUrl))
		self.browser.setFixedHeight(self.customY - 90)
		self.browserFrameLayout.addWidget(self.browser)
		self.layout.addWidget(self.browserFrame)

		# Configure toolbar with navigation actions
		self.configure_toolbar()

		# duplicate this to get it to close
		self.closeButton.deleteLater()
		self.closeButton = QPushButton("X", self)  # Positioned relative to the main widget, not innerFrame
		self.closeButton.setFixedSize(60, 26)
		self.closeButton.setStyleSheet("QPushButton { border: none; background-color: #FFB6C1; font-weight: bold; }")
		self.closeButton.clicked.connect(self.closeWindow)
		# Position the close button in the top right corner of the main widget
		self.closeButton.move(self.width() - self.closeButton.width() - 2, 2)

		self.show()

	def configure_toolbar(self):
		# Back Button
		back_btn = QAction("Back", self)
		back_btn.triggered.connect(self.browser.back)
		self.navtb.addAction(back_btn)

		# Forward Button
		next_btn = QAction("Forward", self)
		next_btn.triggered.connect(self.browser.forward)
		self.navtb.addAction(next_btn)

		# Reload Button
		reload_btn = QAction("Reload", self)
		reload_btn.triggered.connect(self.browser.reload)
		self.navtb.addAction(reload_btn)

		# Stop Button
		stop_btn = QAction("Stop", self)
		stop_btn.triggered.connect(self.browser.stop)
		self.navtb.addAction(stop_btn)

		# URL bar
		self.urlbar = QLineEdit()
		self.urlbar.returnPressed.connect(self.navigate_to_url)
		self.navtb.addWidget(self.urlbar)

	def navigate_to_url(self):
		q = QUrl(self.urlbar.text())
		if q.scheme() == "":
			q.setScheme("http")
		self.browser.setUrl(q)

	def update_title(self):
		title = self.browser.page().title()
		self.setWindowTitle(f"{title} - FFox Browser")

	def update_urlbar(self, q):
		self.urlbar.setText(q.toString())
		self.urlbar.setCursorPosition(0)

	def navigate_home(self):
		self.browser.setUrl(QUrl(self.homeUrl))
