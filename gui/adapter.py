# Copyright (c) 2025
# SPDX-License-Identifier: MIT
# Author: Thomas Harald Reinhard Rubin <thomas.rubin2@protonmail.com>

# Descritpion: This module is an adapter between the gui and backend.


from typing import Union

import numpy as np

from app.app import GuiInterface
from gui.gui import Gui

class GuiAdapter(GuiInterface):
    def __init__(self, gui: Gui):
        self._gui = gui

    # getter for parameter
    def get_selected_number_of_electrodes(self) -> Union[int, None]:
        try:
            return int(self._gui.get_selected_number_of_electrodes())
        except ValueError:
            self.log_message("[ERROR] Invalid number of electrodes value")
            return None

    def get_selected_h0(self) -> Union[float | None]:
        try:
            return float(self._gui.get_selected_h0())
        except ValueError:
            self.log_message("[ERROR] Invalid h0 value")
            return None

    def get_selected_mesh_type(self) -> str:
        return self._gui.get_selected_mesh_type().lower()

    def get_selected_max_area(self) -> float:
        try:
            return float(self._gui.get_selected_max_area())
        except ValueError:
            self.log_message("[ERROR] Invalid max area value")
            return None

    def get_selected_injection_pattern(self) -> str:
        return self._gui.get_selected_injection_pattern()

    def get_selected_serial_port(self) -> str:
        return self._gui.get_selected_serial_port()

    def get_baudrate(self) -> int:
        pass

    # callbacks
    def set_start_button_callback(self, callback: callable):
        self._gui.set_start_button_callback(callback)

    def set_close_callback(self, callback: callable):
        self._gui.set_close_callback(callback)

    # setter for drop down menus
    def set_meshtypes(self, meshtypes: list[str]):
        self._gui.set_meshtypes(meshtypes)

    def set_serial_ports(self, ports: list[str]):
        self._gui.set_serial_ports(ports)

    def set_available_baudrates(self, baudrates: list[int]):
        self._gui.set_available_baudrates([str(baudrate) for baudrate in baudrates])

    def set_available_injection_patterns(self, patterns: list[str]):
        self._gui.set_available_injection_patterns(patterns)

    def set_available_electrode_numbers(self, electrode_numbers: list[int]):
        self._gui.set_available_electrode_numbers([str(number) for number in electrode_numbers])

    # plotting
    def update_heat_map(self, data, el_position: int, mesh_object):
        self._gui.update_heat_map(data,el_position, mesh_object)

    def update_voltage_plot(self, voltages_V: np.ndarray, frequency_Hz: float = 10):
        self._gui.update_voltage_plot(voltages_V, frequency_Hz)

    def set_anomaly_position(self, anomaly_position: int):
        self._gui.set_anomaly_position(str(anomaly_position))

    def log_message(self, message: str):
        self._gui.log_message(message)
