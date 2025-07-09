from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pulse - PC Benchmark & Diagnostics")
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon("assets/icon.png"))  # Replace with your icon

        # Basic layout and label
        layout = QVBoxLayout()
        label = QLabel("Welcome to Pulse!\nSystem performance and diagnostics tool.")
        label.setStyleSheet("font-size: 18px; padding: 20px;")

        layout.addWidget(label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
