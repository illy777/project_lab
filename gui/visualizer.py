from gui.heatmap_display import HeatmapDisplay
from gui.real_time_plot import RealTimePlot

import time
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QSpinBox, QLineEdit, QTextEdit, QSplitter, QFrame
)
from PyQt6.QtCore import Qt
from gui.heatmap_display import HeatmapDisplay
from gui.real_time_plot import RealTimePlot
from app.data_acquire import *
from app.measurement_registry import *
from app.adapters import *

# Main application class
class Visualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyEIT_Thorax GUI")

        # Apply custom stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #0b0f0f;
                color: #00ff99;
                font-family: Courier;
            }
            QLabel {
                color: #80ffc2;
            }
            QComboBox, QSpinBox, QLineEdit {
                background-color: #0b1c1c;
                border: 1px solid #00cc88;
                color: #00ffcc;
            }
            QPushButton {
                background-color: #003f3f;
                border: 1px solid #00ffaa;
                color: #00ffcc;
            }
            QPushButton:hover {
                background-color: #005f5f;
            }
            QTextEdit {
                background-color: #0b1c1c;
                border: 1px solid #00cc88;
                color: #00ffcc;
            }
        """)

        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)

        # Sidebar UI elements
        sidebar = QVBoxLayout()
        sidebar.setSpacing(20)  # Reduce vertical space between widgets
        sidebar.setContentsMargins(50, 4, 4, 200)  # Reduce margins

        sidebar.addWidget(QLabel("Mesh Type"))
        self.mesh_type = QComboBox()
        self.mesh_type.addItems(["Circular", "Forearm", "Lung"])
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
        self.input_electrodes = QSpinBox()
        self.input_electrodes.setRange(1, 64)
        sidebar.addWidget(self.input_electrodes)

        sidebar.addWidget(QLabel("Algorithm"))
        self.algorithm_select = QComboBox()
        self.algorithm_select.addItems(["Gauss-Newton", "Pipeline (GP + DL + Denoising)"])
        sidebar.addWidget(self.algorithm_select)

        sidebar.addWidget(QLabel("Number of Electrodes"))
        self.current_electrodes = QComboBox()
        self.current_electrodes.addItems(["8", "16"])
        sidebar.addWidget(self.current_electrodes)

        sidebar.addWidget(QLabel("Injection Pattern"))
        self.pattern_select = QComboBox()
        self.pattern_select.addItems(["adjacent", "opposite", "skip3", "radial"])
        sidebar.addWidget(self.pattern_select)

        self.run_button = QPushButton("Start Visualization")
        self.run_button.clicked.connect(self.run_visualization)
        sidebar.addWidget(self.run_button)

        # Main area for visual output
        main_area = QVBoxLayout()

        title_label = QLabel("Visual Output")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_area.addWidget(title_label)

        # Horizontal layout with heatmap and plot
        visual_row = QHBoxLayout()
        self.heatmap_display = HeatmapDisplay()
        visual_row.addWidget(self.heatmap_display)
        self.plot_canvas = RealTimePlot()
        visual_row.addWidget(self.plot_canvas)
        main_area.addLayout(visual_row)

        # Anomaly detection log
        anomaly_label = QLabel("Anomaly Detection")
        anomaly_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_area.addWidget(anomaly_label)

        self.visual_output = QTextEdit()
        self.visual_output.setReadOnly(True)
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

    def run_visualization(self):
        self.plot_canvas.paused = False

        meshtype = self.get_mesh_type()
        n_el = self.get_n_electrodes()
        h0 = self.get_h0()
        measurement = Measurement(meshtype, n_el, h0, maxArea=None)
        measurement_interface = FileHandler()
        interface_adapter = InputAdapter()
        data = measurement_interface.readFile("simulation/simulation.txt")
        data_parsed = interface_adapter.parse_data_from_file(data[0])
        result = measurement.do_measurement(data_parsed)
        self.heatmap_display.update_heatmap(ds=result, el_pos=measurement.mesh.el_pos, mesh_obj=measurement.mesh.meshObject)
        self.heatmap_display.show()

        # --- NEW: Update the real-time plot with voltage data from file ---
        try:
            self.plot_canvas.set_voltage_data_from_file(data)
        except Exception as e:
            self.log_message(f"[ERROR] Could not update Voltage vs. Time plot: {e}")

        #self.log_message(f"Pattern:",measurement.measurement._predict_region(result))

        self.log_message("[INFO] Visualization started with parameters:")
        self.log_message(f"Mesh: {self.mesh_type.currentText()}")
        self.log_message(f"h0: {self.h0_input.text()}")
        self.log_message(f"Area: {self.area_input.text()}")
        self.log_message(f"Electrodes: {self.input_electrodes.value()}")
        self.log_message(f"Algorithm: {self.algorithm_select.currentText()}")
        self.log_message(f"Current Electrodes: {self.current_electrodes.currentText()}")
        self.log_message(f"Pattern: {self.pattern_select.currentText()}")

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
        return int(self.current_electrodes.currentText())
    
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