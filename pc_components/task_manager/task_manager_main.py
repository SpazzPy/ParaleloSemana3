import psutil
from matplotlib.ticker import FuncFormatter

import common_vars as cv
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from ui_utils.draggable_widget import DraggableBase
from widgets.widget_base import QWidgetBase

class TaskManagerWindow(DraggableBase, QWidgetBase):
    def __init__(self, icon_name, parent=None, customX=800, customY=400):
        self.customX = customX
        self.customY = customY
        self.icon_name = icon_name
        super().__init__(parent)

        self.cpu_data = []
        self.ram_data = []
        self.disk_data = []

        self.initUI()
        self.startMetricsUpdateTimer()

    def initUI(self):
        self.setupLayouts()
        self.setupGraphs()

    def setupLayouts(self):
        self.containerLayout = QHBoxLayout(self)
        self.containerLayout.setContentsMargins(5, 40, 5, 10)
        self.infoLayout = QVBoxLayout()
        self.graphLayout = QVBoxLayout()

        # Setup for CPU, RAM, and Disk icons and labels
        self.setupIconsAndLabels()

        self.containerLayout.addLayout(self.infoLayout)
        self.containerLayout.addLayout(self.graphLayout)

        # duplicate this to get it to close
        self.closeButton.deleteLater()
        self.closeButton = QPushButton("X", self)  # Positioned relative to the main widget, not innerFrame
        self.closeButton.setFixedSize(60, 26)
        self.closeButton.setStyleSheet("QPushButton { border: none; background-color: #FFB6C1; font-weight: bold; }")
        self.closeButton.clicked.connect(self.closeTaskManager)
        # Position the close button in the top right corner of the main widget
        self.closeButton.move(self.width() - self.closeButton.width() - 2, 2)

    def setupIconsAndLabels(self):
        # Metrics: CPU, RAM, Disk
        metrics = ["cpu", "ram", "disk"]
        icon_paths = [cv.cpu_img, cv.ram_img, cv.disk_img]

        for metric, icon_path in zip(metrics, icon_paths):
            iconLabel = QLabel()
            iconLabel.setPixmap(QPixmap(icon_path).scaled(60, 60))
            textLabel = QLabel(f"{metric.upper()} Usage: 0%")
            layout = QHBoxLayout()
            layout.addWidget(iconLabel)
            layout.addWidget(textLabel)
            self.infoLayout.addLayout(layout)
            setattr(self, f"{metric}Label", textLabel)

    def setupGraphs(self):
        self.figure = Figure(figsize=(4, 4))
        self.canvas = FigureCanvas(self.figure)
        self.graphLayout.addWidget(self.canvas)

        self.ax_cpu = self.figure.add_subplot(311, title="CPU Usage")
        self.ax_ram = self.figure.add_subplot(312, title="RAM Usage")
        self.ax_disk = self.figure.add_subplot(313, title="Disk Usage")

        # Set labels for the axes
        self.set_labels_for_axes()

        # Format Y-axis ticks as integers
        self.format_values()

        # Adjust subplot layout for square graphs
        self.figure.tight_layout()

    def set_labels_for_axes(self):
        self.ax_cpu.set_xlabel("Time")
        self.ax_cpu.set_ylabel("CPU %")
        self.ax_ram.set_xlabel("Time")
        self.ax_ram.set_ylabel("RAM %")
        self.ax_disk.set_xlabel("Time")
        self.ax_disk.set_ylabel("Disk %")

    def format_values(self):
        int_formatter = FuncFormatter(lambda x, _: f'{int(x)}%')
        self.ax_cpu.yaxis.set_major_formatter(int_formatter)
        self.ax_ram.yaxis.set_major_formatter(int_formatter)
        self.ax_disk.yaxis.set_major_formatter(int_formatter)

    def startMetricsUpdateTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateMetrics)
        self.timer.start(1000)

    def updateMetrics(self):
        cpu_usage = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        ram_used = ram.used / (1024 ** 3)
        ram_total = ram.total / (1024 ** 3)
        disk_used = disk.used / (1024 ** 3)
        disk_total = disk.total / (1024 ** 3)

        self.cpuLabel.setText(f"CPU: {cpu_usage}%")
        self.ramLabel.setText(f"RAM: {ram.percent}%, {ram_used:.2f}/{ram_total:.2f} GB")
        self.diskLabel.setText(f"Disk: {disk.percent}%, {disk_used:.2f}/{disk_total:.2f} GB")

        self.cpu_data.append(cpu_usage)
        self.ram_data.append(ram.percent)
        self.disk_data.append(disk.percent)

        self.cpu_data = self.cpu_data[-20:]
        self.ram_data = self.ram_data[-20:]
        self.disk_data = self.disk_data[-20:]

        self.ax_cpu.clear()
        self.ax_ram.clear()
        self.ax_disk.clear()

        self.ax_cpu.plot(self.cpu_data)
        self.ax_ram.plot(self.ram_data)
        self.ax_disk.plot(self.disk_data)

        self.set_labels_for_axes()

        self.format_values()

        self.ax_cpu.set_title("CPU Usage")
        self.ax_ram.set_title("RAM Usage")
        self.ax_disk.set_title("Disk Usage")

        self.canvas.draw()

    def closeTaskManager(self):
        # Stop the update timer
        if self.timer.isActive():
            self.timer.stop()

        # Clear the matplotlib figure to ensure it's properly closed
        self.figure.clear()

        # Properly delete the canvas widget to release resources
        self.canvas.deleteLater()

        # Call the superclass close method to close the window
        super().close()


