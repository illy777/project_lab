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
        fig = Figure(figsize=(3, 3), dpi=100, facecolor='#ffffff')
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)

        # Set background color to black
        self.ax.set_facecolor('#ffffff')
        fig.patch.set_facecolor('#ffffff')

        # Initialize plot data for 40 samples (Voltage vs. Time)
        self.x_data = np.arange(40)
        self.y_data = np.zeros(40)
        self.line, = self.ax.plot(self.x_data, self.y_data, 'g-')  # green line

        # Set axis and label colors to green
        self.ax.tick_params(axis='x', colors='black')
        self.ax.tick_params(axis='y', colors='black')
        self.ax.xaxis.label.set_color('black')
        self.ax.yaxis.label.set_color('black')
        self.ax.title.set_color('black')
        self.ax.spines['bottom'].set_color('black')
        self.ax.spines['top'].set_color('black')
        self.ax.spines['right'].set_color('black')
        self.ax.spines['left'].set_color('black')

        # Show dimmed grid lines
        self.ax.grid(True, color='black', alpha=0.50, linewidth=0.9)
        
        self.ymax = 6
        self.ymin = 0
        self.line.set_color('black')
        self.line.set_linewidth(2)
        self.ax.set_ylim(self.ymin, self.ymax)
        self.ax.set_xlim(0, 39)
        self.ax.set_xlabel("Time (sample index)", fontsize=18)
        self.ax.set_ylabel("Voltage (V)", fontsize=18)

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
            if min_voltage >= -1:
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