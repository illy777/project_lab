# Copyright (c) 2025 
# SPDX-License-Identifier: MIT
# Author: Ömer Faruk KANMAZ <kanmazomerfaruk@outlook.com>
#
# Descritpion: This module is the real-time voltage plot widget for the EIT system 
# Module using PyQt6 and matplotlib for rendering.

from PyQt6.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

# Real-time plot widget using matplotlib
class VoltagePlot(FigureCanvas):
    def __init__(self, parent=None):
        # Set up the matplotlib figure and axis
        fig = Figure(figsize=(5, 3), dpi=100, facecolor='black')
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

        # Set background color to black
        self.ax.set_facecolor('black')
        fig.patch.set_facecolor('black')

        # Initialize plot data for 40 samples (Voltage vs. Time)
        self.x_data = np.arange(40)
        self.y_data = np.zeros(40)
        self.line, = self.ax.plot(self.x_data, self.y_data, 'g-')  # green line

        # Set axis and label colors to green
        self.ax.tick_params(axis='x', colors='lime')
        self.ax.tick_params(axis='y', colors='lime')
        self.ax.xaxis.label.set_color('lime')
        self.ax.yaxis.label.set_color('lime')
        self.ax.title.set_color('lime')
        self.ax.spines['bottom'].set_color('lime')
        self.ax.spines['top'].set_color('lime')
        self.ax.spines['right'].set_color('lime')
        self.ax.spines['left'].set_color('lime')

        # Show dimmed grid lines
        self.ax.grid(True, color='lime', alpha=0.15, linewidth=0.8)
        
        self.ymax = 6
        self.ymin = 0
        self.ax.set_ylim(self.ymin, self.ymax)
        self.ax.set_xlim(0, 39)
        self.ax.set_xlabel("Time (sample index)")
        self.ax.set_ylabel("Voltage (V)")

        self.paused = True  # Start in paused state

    def update_plot(self, voltages):
        voltages = np.array(voltages, dtype=float)
        if voltages.size == 0:
            raise ValueError("Input voltages must be a non-empty array or list.")
        # Update the y-axis limits if necessary
        max_voltage = np.max(voltages) + 1
        min_voltage = np.min(voltages) - 1
        if max_voltage > self.ymax:
            self.ymax = max_voltage
        if min_voltage < self.ymin:
            if min_voltage >= 0:
                self.ymin = 0
            else:
                self.ymin = min_voltage
        self.ax.set_ylim(self.ymin, self.ymax)

        # Scroll the plot: shift left and append new value(s)
        n = len(voltages)
        if n > len(self.y_data):
            # If more than 40, just take the last 40
            self.y_data = voltages[-40:]
        else:
            self.y_data = np.roll(self.y_data, -n)
            self.y_data[-n:] = voltages
        self.line.set_ydata(self.y_data)
        self.draw()
       
    def toggle_pause(self):
        self.paused = not self.paused