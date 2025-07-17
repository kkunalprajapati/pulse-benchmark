from PySide6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, QGroupBox,
    QFormLayout, QScrollArea, QProgressBar, QPushButton,
    QTabWidget, QApplication,QHBoxLayout, QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt
from PySide6.QtCore import QThread
from core.benchmark_worker import BenchmarkWorker

from core.system_info import get_system_info
# from core.benchmark import run_benchmark, export_benchmark_report

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
        # Benchmark Mode Toggle
        mode_label = QLabel("Select Benchmark Mode:")
        mode_label.setStyleSheet("font-size: 13px; color: black; padding-bottom: 5px;")
        
        self.quick_mode = QRadioButton("Quick")
        self.full_mode = QRadioButton("Complete")
        self.quick_mode.setChecked(True)
        
        mode_group = QButtonGroup()
        mode_group.addButton(self.quick_mode)
        mode_group.addButton(self.full_mode)
        
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.quick_mode)
        mode_layout.addWidget(self.full_mode)
        mode_layout.addStretch()
        # Score bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 10)
        layout.addWidget(self.progress_bar)

        # Button
        btn = QPushButton("Run Benchmark")
        btn.clicked.connect(self.handle_benchmark)
        layout.addWidget(btn)

        export_btn = QPushButton("Save Report")
        export_btn.clicked.connect(self.export_benchmark)

        self.export_status = QLabel("")
        self.export_status.setStyleSheet("font-size: 12px; color: #7fff7f;")

        layout.addWidget(export_btn)
        layout.addWidget(self.export_status)
        

        layout.addLayout(mode_layout)

        widget.setLayout(layout)
        return widget

    def handle_benchmark(self):
        self.result_label.setText("Running benchmark...")
        self.progress_bar.setValue(0)

        mode = "quick" if self.quick_mode.isChecked() else "complete"

        self.thread = QThread()
        self.worker = BenchmarkWorker(mode)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.result.connect(self.display_results)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

       
    def display_results(self, results):
        self.latest_benchmark = results
        score = results["Final Score"]
    
        self.result_label.setText(
            f"🧠 CPU (Single-Core): {results['CPU Single-Core']} hashes/sec\n"
            f"⚙️ CPU (Multi-Core): {results['CPU Multi-Core']} hashes/sec\n"
            f"📊 RAM Speed: {results['RAM Speed']} MB/s\n"
            f"💾 Disk Write: {results['Disk Write']} MB/s\n"
            f"💾 Disk Read: {results['Disk Read']} MB/s\n"
            f"🏁 Overall Score: {score} / 10"
        )
        self.score_display.setText(f"⚙️ {score} / 10")

    def export_benchmark(self):
        if hasattr(self, "latest_benchmark"):
            path = export_benchmark_report(self.latest_benchmark, format="json")
            self.export_status.setText(f"Report saved to: {path}")
        else:
            self.export_status.setText("Run a benchmark first.")
    
   