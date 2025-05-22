import numpy as np
from PyQt6.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Real-time plot widget using matplotlib
class RealTimePlot(FigureCanvas):
    def __init__(self, parent=None):
        # Set up the matplotlib figure and axis
        fig = Figure(figsize=(5, 3), dpi=100)
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

        # Initialize plot data for 40 samples (Voltage vs. Time)
        self.x_data = np.arange(40)
        self.y_data = np.zeros(40)
        self.line, = self.ax.plot(self.x_data, self.y_data, 'g-')
        self.ax.set_ylim(0, 5)
        self.ax.set_xlim(0, 39)
        self.ax.set_xlabel("Time (sample index)")
        self.ax.set_ylabel("Voltage (V)")
        self.ax.set_title("Voltage vs. Time")

        self.paused = True  # Start in paused state
        
        """
        # Timer to periodically update plot (optional for real-time)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)
        """

    def set_voltage_data_from_file(self, file_data):
        if not file_data or not isinstance(file_data, list):
            raise ValueError("Input data must be a non-empty list of strings.")
        try:
            voltage_values = [float(x) for x in file_data[0].split()]
        except Exception:
            raise ValueError("Could not parse voltage values from file data.")
        if len(voltage_values) != 40:
            raise ValueError("Voltage data pack must contain exactly 40 values.")
        self.y_data = np.array(voltage_values)
        self.line.set_ydata(self.y_data)
        self.draw()

    def update_plot(self):
        self.line.set_ydata(self.y_data)
        self.draw()

    def toggle_pause(self):
        self.paused = not self.paused