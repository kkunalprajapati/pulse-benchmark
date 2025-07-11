from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QGroupBox, QFormLayout, QScrollArea
from core.system_info import get_system_info

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pulse – System Information")
        self.setMinimumSize(900, 600)

        # Scrollable layout
        scroll = QScrollArea()
        widget = QWidget()
        layout = QVBoxLayout(widget)

        system_info = get_system_info()

        
        for section, data in system_info.items():
            group_box = QGroupBox(section)
            form_layout = QFormLayout()
            for key, value in data.items():
                form_layout.addRow(f"{key}:", QLabel(str(value)))
            group_box.setLayout(form_layout)
            layout.addWidget(group_box)

        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        self.setCentralWidget(scroll)
