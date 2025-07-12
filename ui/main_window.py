from PySide6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, QGroupBox,
    QFormLayout, QScrollArea, QProgressBar, QPushButton,
    QTabWidget, QApplication
)
from PySide6.QtCore import Qt

from core.system_info import get_system_info
from core.benchmark import run_benchmark

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pulse – Benchmark & Diagnostics")
        self.setMinimumSize(900, 600)

        tabs = QTabWidget()
        tabs.addTab(self.create_system_info_tab(), "System Info")
        tabs.addTab(self.create_benchmark_tab(), "Benchmark")

        self.setCentralWidget(tabs)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
                color: #f0f0f0;
            }
            QLabel {
                font-size: 15px;
                color: #e0e0e0;
            }
            QGroupBox {
                border: 1px solid #444;
                border-radius: 10px;
                margin-top: 12px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
            }
            QFormLayout > QLabel {
                font-size: 14px;
            }
            QProgressBar {
                background-color: #2e2e2e;
                border-radius: 6px;
                height: 24px;
                font-size: 14px;
            }
            QProgressBar::chunk {
                background-color: #00ffaa;
                border-radius: 5px;
                margin: 1px;
            }
            QPushButton {
                background-color: #1e88e5;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
        """)
        

    def create_system_info_tab(self):
        container = QWidget()               # Container for the scroll area
        layout = QVBoxLayout(container)     # Main vertical layout

        system_info = get_system_info()
        for section, data in system_info.items():
            group_box = QGroupBox(section)
            form_layout = QFormLayout()

            for key, value in data.items():
                key_label = QLabel(f"{key}:")
                key_label.setStyleSheet("font-size: 14px; color: black; padding-right: 6px;")
                value_label = QLabel(str(value))
                value_label.setStyleSheet("font-size: 14px; color: black;")
                form_layout.addRow(key_label, value_label)

            group_box.setLayout(form_layout)
            layout.addWidget(group_box)

        layout.addStretch()  # Keeps spacing clean at the bottom

        # Scrollable area setup
        scroll_area = QScrollArea()
        scroll_area.setWidget(container)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        return scroll_area
    
    def create_benchmark_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        # Score display (big circle)

        self.score_display = QLabel("⚙️ 0 / 10")
        self.score_display.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #00ffaa;
            qproperty-alignment: AlignCenter;
            padding: 10px;
        """)
        layout.addWidget(self.score_display)

        # Detailed result text
        self.result_label = QLabel("Click 'Run Benchmark' to begin.")
        self.result_label.setStyleSheet("font-size: 14px; padding: 10px; color: black;")
        layout.addWidget(self.result_label)

        # Score bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 10)
        layout.addWidget(self.progress_bar)

        # Button
        btn = QPushButton("Run Benchmark")
        btn.clicked.connect(self.handle_benchmark)
        layout.addWidget(btn)

        widget.setLayout(layout)
        return widget

    def handle_benchmark(self):
        self.result_label.setText("Benchmarking... please wait.")
        QApplication.processEvents()
        results = run_benchmark()
    
        score = results["Final Score"]
        self.progress_bar.setValue(int(score))
        self.result_label.setText(
            f"🔍 CPU Score: {results['CPU Score']}\n"
            f"📊 RAM Score: {results['RAM Score']}\n"
            f"🎯 Final Score: {score} / 10"
        )
        self.score_display.setText(f"⚙️ {score} / 10")