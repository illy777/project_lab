# Copyright (c) 2025
# SPDX-License-Identifier: MIT
# Author: Ömer Faruk KANMAZ <kanmazomerfaruk@outlook.com>
# Author: Thomas Harald Reinhard Rubin <thomas.rubin2@protonmail.com>
#
# Descritpion: This module is the main GUI for the application.
## It provides a user interface for the EIT system, allowing users to configure parameters, visualize data, and interact with the system.

import threading, time, os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy,
    QLabel, QComboBox, QSpinBox, QLineEdit, QTextEdit, QSplitter, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPixmap, QIcon,QTextCursor

from gui.heatmap_display import HeatmapDisplay
from gui.voltage_plot import VoltagePlot
import numpy as np

# Main application class
class Gui(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyEIT_Thorax GUI")
        self.run_button_callback = None
        self.close_callback = None
        self.data_lock = threading.Lock()
        self.ds= None
        self.mesh_obj= None
        self.el_pos= None
        self.voltages_V = None
        self.voltages_data_lock = threading.Lock()
        self.frequency_Hz = None
        self.anomaly_position = None
        self.new_hatmap_data = False
        self.new_voltage_data = False
        self.last_logged_anomaly_position = None

        # daemon -> just terminate when program exits, will not continue to run in background
        self.visualization_thread = threading.Thread(target=self.run_visualization, daemon=True)

        self.setStyleSheet("""
            QWidget {
                font-size: 12px;
                background-color: #0b0f0f;
                color: #00ff99;
                font-family: Courier;
            }
            QLabel {
                font-size: 20px;
                color: #80ffc2;
                background-color: #000000;
            }
            QComboBox, QSpinBox, QLineEdit {
                font-size: 20px;
                background-color: #000000;
                border: 1px solid #00cc88;
                color: #00ffcc;
            }
            QPushButton {
                font-size: 16px;
                background-color: #000000;
                border: 1px solid #00ffaa;
                color: #00ffcc;
            }
            QPushButton:hover {
                background-color: #005f5f;
            }
            QTextEdit {
                font-size: 20px;
                bold: true;
                background-color: #000000;
                border: 1px solid #00cc88;
                color: #00ffcc;
            }
        """)
        # Load background image
        self.background_pixmap = QPixmap(os.path.join(os.getcwd(), 'gui', 'background.png'))
        self.setup_ui()

    def closeEvent(self, event):
        if self.close_callback is None:
            raise RuntimeError("Close callback for backend is not set!")
        else:
            self.close_callback()

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
        sidebar.setContentsMargins(4, 4, 8, 50)  # Reduce margins

        sidebar.addWidget(QLabel("Mesh Type"))
        self.mesh_type = QComboBox()
        sidebar.addWidget(self.mesh_type)

        sidebar.addWidget(QLabel("Serial Port"))
        self.serial_ports = QComboBox()
        sidebar.addWidget(self.serial_ports)

        sidebar.addWidget(QLabel("Baudrate"))
        self.baudrates = QComboBox()
        sidebar.addWidget(self.baudrates)

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

        

        sidebar.addWidget(QLabel("Number of Electrodes"))
        self.num_electrodes = QComboBox()
        sidebar.addWidget(self.num_electrodes)

        sidebar.addWidget(QLabel("Injection Pattern"))
        self.pattern_select = QComboBox()
        sidebar.addWidget(self.pattern_select)

        self.run_button = QPushButton("Start Visualization")
        self.run_button.setCheckable(True)
        self.run_button.setMinimumHeight(48)
        self.run_button.setStyleSheet("font-size: 18px;")
        self.run_button.clicked.connect(self.toggle_visualization)
        sidebar.addWidget(self.run_button)

        self.region_of_anomaly = QLabel()
        anomaly_pixmap = QPixmap(os.path.join(os.getcwd(), 'gui', 'regions_of_anomaly.jpeg'))
        self.region_of_anomaly.setPixmap(anomaly_pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.region_of_anomaly.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.region_of_anomaly.hide()  # Hide by default, show when needed
        sidebar.addWidget(self.region_of_anomaly)
        self.anomaly_figure_label = QLabel("Reference for Regions of Anomaly")
        self.anomaly_figure_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.anomaly_figure_label.setStyleSheet("font-size: 12px; color: #80ffc2; background-color: transparent;")
        sidebar.addWidget(self.anomaly_figure_label)
        self.anomaly_figure_label.hide()  # Hide by default, show when needed

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
            
            if self.mesh_type.currentText().lower() == "circular":
                self.region_of_anomaly.show()
                self.anomaly_figure_label.show()
            else:
                self.region_of_anomaly.hide()
                self.anomaly_figure_label.hide()

        self.mesh_type.currentIndexChanged.connect(on_mesh_type_changed)
        # Call once to set initial state
        on_mesh_type_changed(self.mesh_type.currentIndex())

        # Main area for visual output
        main_area = QVBoxLayout()

        title_label = QLabel("Visual Output")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_area.addWidget(title_label)

        # Horizontal layout with heatmap and plot
        visual_row = QHBoxLayout()

        #Todo: When resizing verical axis delays...
        self.heatmap_display = HeatmapDisplay()
        self.heatmap_display.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.heatmap_width = self.heatmap_display.width()
        self.heatmap_height = self.heatmap_display.height()
        self.heatmap_display.setMinimumSize(350, 350)
        self.heatmap_display.setMaximumSize(800, 800)
        visual_row.addWidget(self.heatmap_display)

        self.plot_canvas = VoltagePlot()
        self.plot_canvas.setMinimumSize(450, 450)
        self.plot_canvas.setMaximumSize(700, 700)
        visual_row.addWidget(self.plot_canvas)
        main_area.addLayout(visual_row)

        # Anomaly detection log (make this area smaller in height)
        anomaly_label = QLabel("Anomaly Detection")
        anomaly_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_area.addWidget(anomaly_label)

        self.visual_output = QTextEdit()
        self.visual_output.setReadOnly(True)
        # Reduce the height of anomaly detection area
        self.visual_output.setFixedHeight(200)  # Smaller height for anomaly detection log
        main_area.addWidget(self.visual_output)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar)
        sidebar_widget.setMaximumWidth(280)
        main_widget = QWidget()
        main_widget.setLayout(main_area)

        splitter.addWidget(sidebar_widget)
        splitter.addWidget(main_widget)

        # Create a container layout for the toggle button and the splitter
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(splitter)

        main_layout.addLayout(container_layout)

        # Add the toggle button outside the sidebar, bottom left
        self.toggle_sidebar_btn = QPushButton()
        self.toggle_sidebar_btn.setText("☰")
        self.toggle_sidebar_btn.setIcon(QIcon())  # Remove icon if set
        self.toggle_sidebar_btn.setCheckable(True)
        self.toggle_sidebar_btn.setChecked(True)
        self.toggle_sidebar_btn.setFixedSize(20, 20)
        self.toggle_sidebar_btn.clicked.connect(lambda: sidebar_widget.setVisible(self.toggle_sidebar_btn.isChecked()))
        # Toggle button using absolute positioning:
        self.toggle_sidebar_btn.setParent(self)
        self.toggle_sidebar_btn.move(10, self.height() - 30)  # Bottom left
        self.toggle_sidebar_btn.show()

    # Keep the toggle button at the bottom left corner when resizing
    def resizeEvent(self, event):
        super().resizeEvent(event)
        btn_margin = 10
        self.toggle_sidebar_btn.move(btn_margin, self.height() - self.toggle_sidebar_btn.height() - btn_margin)        

    def toggle_visualization(self):
        self.run_button_callback(self.run_button.isChecked())

        if self.run_button.isChecked():
            self.run_button.setText("Visualizing...")
            self.log_message(f"""[INFO] Visualization started with parameters:
                    Mesh: {self.mesh_type.currentText()}
                    h0: {self.h0_input.text()}
                    Number of Electrodes: {self.num_electrodes.currentText()}
                    Pattern: {self.pattern_select.currentText()}""")
            if not self.visualization_thread.is_alive():
                self.visualization_thread.start()
        else:
            self.run_button.setText("Start Visualization")

    def run_visualization(self):
        while True:
            if self.new_hatmap_data:
                with self.data_lock:
                    self.heatmap_display.update_heatmap_opencv(self.ds, self.mesh_obj, self.el_pos, self.heatmap_height, self.heatmap_width)
                self.new_hatmap_data = False
                self.heatmap_display.show()

                # Only log if anomaly_position changed
                if self.anomaly_position != self.last_logged_anomaly_position:
                    self.last_logged_anomaly_position = self.anomaly_position
                    self.log_message(f"Anomaly position: Region {self.anomaly_position}")

            if self.new_voltage_data:
                with self.voltages_data_lock:
                    self.plot_canvas.update_plot(self.voltages_V)
                self.new_voltage_data = False
                self.plot_canvas.show()
            time.sleep(0.1)  # Adjust sleep time as needed for performance

    # Getters for parameters
    def get_selected_number_of_electrodes(self) -> str:
        return self.num_electrodes.currentText()

    def get_selected_h0(self) -> str:
        return self.h0_input.text()

    def get_selected_mesh_type(self) -> str:
        return self.mesh_type.currentText()

    def get_selected_max_area(self) -> str:
        return self.area_input.text()

    def get_selected_injection_pattern(self) -> str:
        return self.pattern_select.currentText().lower()

    def get_selected_serial_port(self) -> str:
        return self.serial_ports.currentText()

    def get_baudrate(self) -> str:
        return self.baudrates.currentText()

    # set callbacks
    def set_start_button_callback(self, callback: callable):
        self.run_button_callback = callback

    def set_close_callback(self, callback: callable):
        self.close_callback = callback

    # setters for drop down menus
    def set_meshtypes(self, meshtypes: list[str]):
        self.mesh_type.clear()
        capitalized_meshtypes = [m.capitalize() for m in meshtypes]
        meshtypes = sorted(capitalized_meshtypes, key=lambda x: x.lower())  # Sort alphabetically
        self.mesh_type.addItems(meshtypes)

    def set_serial_ports(self, ports: list[str]):
        self.serial_ports.clear()
        self.serial_ports.addItems(ports)

    def set_available_baudrates(self, baudrates: list[str]):
        self.baudrates.clear()
        self.baudrates.addItems(baudrates)

    def set_available_injection_patterns(self, patterns: list[str]):
        self.pattern_select.clear()
        capitalized_patterns = [p.capitalize() for p in patterns]
        patterns = sorted(capitalized_patterns, key=lambda x: x.lower())
        self.pattern_select.addItems(patterns)

    def set_available_electrode_numbers(self, electrode_numbers: list[str]):
        self.num_electrodes.clear()
        self.num_electrodes.addItems(electrode_numbers)

    # plotting
    def update_heat_map(self, data, el_position: int, mesh_object):
        with self.data_lock:
            self.ds = data
            self.el_pos = el_position
            self.mesh_obj = mesh_object
            self.new_hatmap_data = True

    def update_voltage_plot(self, voltages_V: np.ndarray, frequency_Hz: float = 10):
        with self.voltages_data_lock:
            self.voltages_V = voltages_V
            self.frequency_Hz = frequency_Hz
            self.new_voltage_data = True

    def set_anomaly_position(self, anomaly_position: str):
        self.anomaly_position = anomaly_position

    def log_message(self, msg):
        timestamp = time.strftime("[%H:%M:%S]")
        self.visual_output.append(f"{timestamp} {msg}")

    # Limit log to last 100 lines
        max_lines = 100
        doc = self.visual_output.document()
        while doc.blockCount() > max_lines:
            cursor = self.visual_output.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            cursor.select(QTextCursor.SelectionType.LineUnderCursor)
            cursor.removeSelectedText()
            cursor.deleteChar()