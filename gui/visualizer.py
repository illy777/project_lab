import time
import threading
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QSpinBox, QLineEdit, QTextEdit, QSplitter, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPixmap
from app.builder import Pipeline_Builder
from gui.heatmap_display import HeatmapDisplay
from gui.real_time_plot import RealTimePlot
from app.data_acquire import *


# Main application class
class Gui(QWidget):
    def __init__(self, mesh_types=None):
        super().__init__()
        self.mesh_types = mesh_types or []
        self.setWindowTitle("PyEIT_Thorax GUI")

        # Remove background-image from stylesheet, keep only colors for widgets
        self.setStyleSheet("""
            QWidget {
                background-color: #0b0f0f;
                color: #00ff99;
                font-family: Courier;
            }
            QLabel {
                color: #80ffc2;
                background-color: #000000;
            }
            QComboBox, QSpinBox, QLineEdit {
                background-color: #000000;
                border: 1px solid #00cc88;
                color: #00ffcc;
            }
            QPushButton {
                background-color: #000000;
                border: 1px solid #00ffaa;
                color: #00ffcc;
            }
            QPushButton:hover {
                background-color: #005f5f;
            }
            QTextEdit {
                background-color: #000000;
                border: 1px solid #00cc88;
                color: #00ffcc;
            }
        """)

        self.background_pixmap = QPixmap("/Users/omerfarukkanmaz/Desktop/Uni/project_lab/project_lab/gui/background.png")
        self.setup_ui()

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.background_pixmap.isNull():
            # Scale the pixmap to widget size
            painter.drawPixmap(self.rect(), self.background_pixmap)
        super().paintEvent(event)

    def setup_ui(self):
        main_layout = QHBoxLayout(self)

        # Sidebar UI elements
        sidebar = QVBoxLayout()
        sidebar.setSpacing(20)  # Reduce vertical space between widgets
        sidebar.setContentsMargins(50, 4, 4, 200)  # Reduce margins

        sidebar.addWidget(QLabel("Mesh Type"))
        self.mesh_type = QComboBox()
        self.mesh_type.addItems(self.mesh_types)
        sidebar.addWidget(self.mesh_type)

         # Area input for Lung mesh type only
        self.area_label = QLabel("Max Area (Lung)")
        self.area_input = QLineEdit()
        self.area_label.hide()
        self.area_input.hide()
        sidebar.addWidget(self.area_label)
        sidebar.addWidget(self.area_input)

        self.h0_label = QLabel("h0")
        sidebar.addWidget(self.h0_label)
        self.h0_input = QLineEdit()
        self.h0_input.setText("0.07")  # Set default value to 0.07
        sidebar.addWidget(self.h0_input)

        # Show Max Area Lung and hide h0 input based on mesh type selection
        def on_mesh_type_changed(index):
            if self.mesh_type.currentText().lower() == "lung":
                self.area_label.show()
                self.area_input.show()
                self.h0_label.hide()
                self.h0_input.hide()
            else:
                self.area_label.hide()
                self.area_input.hide()
                self.h0_label.show()
                self.h0_input.show()
                
        self.mesh_type.currentIndexChanged.connect(on_mesh_type_changed)
        # Call once to set initial state
        on_mesh_type_changed(self.mesh_type.currentIndex())


        sidebar.addWidget(QLabel("Input Electrodes"))
        self.el_pos = QSpinBox()
        self.el_pos.setRange(1, 64)
        sidebar.addWidget(self.el_pos)

        sidebar.addWidget(QLabel("Algorithm"))
        self.algorithm_select = QComboBox()
        self.algorithm_select.addItems(["Gauss-Newton", "Pipeline (GP + DL + Denoising)"])
        sidebar.addWidget(self.algorithm_select)

        sidebar.addWidget(QLabel("Number of Electrodes"))
        self.num_electrodes = QComboBox()
        self.num_electrodes.addItems(["8", "16"])
        sidebar.addWidget(self.num_electrodes)

        sidebar.addWidget(QLabel("Injection Pattern"))
        self.pattern_select = QComboBox()
        self.pattern_select.addItems(["Adjacent", "Opposite", "Skip-3", "Radial"])
        sidebar.addWidget(self.pattern_select)

        self.run_button = QPushButton("Start Visualization")
        self.run_button.setCheckable(True)
        self.run_button.clicked.connect(self.toggle_visualization)
        sidebar.addWidget(self.run_button)

        # Main area for visual output
        main_area = QVBoxLayout()

        title_label = QLabel("Visual Output")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_area.addWidget(title_label)

        # Horizontal layout with heatmap and plot
        visual_row = QHBoxLayout()
        self.heatmap_display = HeatmapDisplay()
        self.heatmap_display.setMinimumHeight(350)
        self.heatmap_display.setMinimumWidth(350)
        visual_row.addWidget(self.heatmap_display, stretch=2)
        self.plot_canvas = RealTimePlot()
        self.plot_canvas.setMinimumHeight(350)
        self.plot_canvas.setMinimumWidth(350)
        visual_row.addWidget(self.plot_canvas, stretch=2)
        main_area.addLayout(visual_row)

        # Anomaly detection log (make this area smaller in height)
        anomaly_label = QLabel("Anomaly Detection")
        anomaly_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_area.addWidget(anomaly_label)

        self.visual_output = QTextEdit()
        self.visual_output.setReadOnly(True)
        # Reduce the height of anomaly detection area
        self.visual_output.setFixedHeight(200)  # Smaller height for anomaly detection log
        main_area.addWidget(self.visual_output)

        self.command_line = QLineEdit()
        self.command_line.setPlaceholderText("Enter command or parameter (e.g. set h0=0.15)")
        self.command_line.returnPressed.connect(self.handle_command)
        main_area.addWidget(self.command_line)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar)
        main_widget = QWidget()
        main_widget.setLayout(main_area)

        splitter.addWidget(sidebar_widget)
        splitter.addWidget(main_widget)
        main_layout.addWidget(splitter)

    def toggle_visualization(self):
        if self.run_button.isChecked():
            self.run_button.setText("Visualizing...")
            #self.visualization_thread = threading.Thread(target=self.run_visualization, daemon=True)
            self.run_visualization()
            #self.visualization_thread.start()
        else:
            self.run_button.setText("Start Visualization")

    def run_visualization(self):
        self.plot_canvas.paused = False

        self.log_message(f"""[INFO] Visualization started with parameters:
                Mesh: {self.mesh_type.currentText()}
                h0: {self.h0_input.text()}
                Input Electrodes: {self.el_pos.value()}
                Number of Electrodes: {self.num_electrodes.currentText()}
                Pattern: {self.pattern_select.currentText()}""")

                
    def handle_command(self):
        command = self.command_line.text().strip()
        if command.startswith("set "):
            try:
                key, value = command[4:].split("=")
                getattr(self, f"{key}_input").setText(value)
                self.log_message(f"[CMD] Set {key} to {value}")
            except Exception:
                self.log_message(f"[ERROR] Invalid command: {command}")
        else:
            self.log_message(f"[CMD] Unknown command: {command}")
        self.command_line.clear()

    def log_message(self, msg):
        timestamp = time.strftime("[%H:%M:%S]")
        self.visual_output.append(f"{timestamp} {msg}")
        self.visual_output.verticalScrollBar().setValue(self.visual_output.verticalScrollBar().maximum())
    
    #Getters for parameters
    def get_mesh_type(self):
        return self.mesh_type.currentText().lower()
    
    def get_n_electrodes(self):
        return int(self.num_electrodes.currentText())
    
    def get_h0(self):
        try:
            return float(self.h0_input.text())
        except ValueError:
            self.log_message("[ERROR] Invalid h0 value")
            return None
        
    def get_max_area(self):
        try:
            return float(self.area_input.text())
        except ValueError:
            self.log_message("[ERROR] Invalid max area value")
            return None
    def get_pattern(self):
        return self.pattern_select.currentText().lower()
        
    def get_algorithm(self):
        return self.algorithm_select.currentText().lower()
    def get_el_pos(self):
        return self.el_pos.value()