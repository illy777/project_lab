# Copyright (c) 2025
# SPDX-License-Identifier: MIT
# Author: Thomas Harald Reinhard Rubin <thomas.rubin2@protonmail.com>
# Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
#
# Descritpion: This module is the main Interface between the GUI and the backend EIT system.
# This module is the overseer for the EIT system, managing the GUI, data acquisition, and pipeline execution.
import threading
from abc import abstractmethod
from abc import ABC
import time
from typing import Union

from app.factory import Pipeline
from app.data_types import *

import numpy as np

TIMEOUT_S = 5

class GuiInterface(ABC):
    # getter for current selection in gui
    @abstractmethod
    def get_selected_number_of_electrodes(self) -> Union[int, None]:
        pass

    @abstractmethod
    def get_selected_h0(self) -> Union[float, None]:
        pass

    @abstractmethod
    def get_selected_mesh_type(self) -> str:
        pass

    @abstractmethod
    def get_selected_max_area(self) -> Union[float, None]:
        pass

    @abstractmethod
    def get_selected_injection_pattern(self) -> str:
        pass

    @abstractmethod
    def get_selected_serial_port(self) -> str:
        pass

    @abstractmethod
    def get_selected_baudrate(self) -> Union[int | None]:
        pass

    # callbacks
    @abstractmethod
    def set_start_button_callback(self, callback: callable):
        pass

    @abstractmethod
    def set_close_callback(self, callback: callable):
        pass

    # setter for selectable widgets
    @abstractmethod
    def set_meshtypes(self, meshtypes: list[str]):
        pass

    @abstractmethod
    def set_serial_ports(self, ports: list[str]):
        pass

    @abstractmethod
    def set_available_baudrates(self, baudrates: list[int]):
        pass

    @abstractmethod
    def set_available_injection_patterns(self, patterns: list[str]):
        pass

    @abstractmethod
    def set_available_electrode_numbers(self, electrode_numbers: list[int]):
        pass

    # plotting
    @abstractmethod
    def update_heat_map(self, data, el_position: int, mesh_object):
        pass

    @abstractmethod
    def update_voltage_plot(self, voltages_V: np.ndarray, frequency_Hz: float = 10):
        pass

    # setter for display
    @abstractmethod
    def set_anomaly_position(self, anomaly_position: int):
        pass

    # logging
    @abstractmethod
    def log_message(self, message: str):
        pass

class DataAcquirerInterface(ABC):

    @abstractmethod
    def connect(self, timeout:int):
        """This method should be implemented in the derived class."""
        pass
    @abstractmethod
    def disconnect(self):
        """This method should be implemented in the derived class."""
        pass
    @abstractmethod
    def acquire_data(self, timeout:int) -> np.ndarray:
        """This method should be implemented in the derived class."""
        pass
    @abstractmethod
    def get_serial_ports(self) -> list[str]:
        """This method should return a list of available serial ports."""
        pass
    @abstractmethod
    def get_available_baudrates(self) -> list[int]:
        """This method should return a list of available baud rates."""
        pass
    @abstractmethod
    def set_serial_port(self, port: str):
        """This method should set the serial port."""
        pass
    @abstractmethod
    def set_baudrate(self, baudrate: int):
        """This method should set the baud rate."""
        pass

class PipelineBuilderInterface(ABC):
    @abstractmethod
    def build_pipeline(self, meshtype: str, n_el: ElectrodeNumber, h0: float, maxArea: float, injection_pattern: InjectionPattern) -> Pipeline:
        pass

class RegistryInterface(ABC):
    @abstractmethod
    def get_meshtypes(self) -> list[str]:
        pass

    # ToDo: add interface methods for builder to work properly

class Sentinel:
    def __init__(self, gui_interface: GuiInterface, data_acquirer_interface: DataAcquirerInterface,
                 pipeline_builder_interface: PipelineBuilderInterface,
                 registry_interface: RegistryInterface):
        self._gui = gui_interface
        self._dataAcquirer = data_acquirer_interface
        self._pipeline_builder = pipeline_builder_interface
        self._registry = registry_interface
        self._pipeline = None
        self._connected: bool = False

        self._executing_measurement: bool = False

        # don't be daemonic, so that python program can't be exited without this exiting thread
        self._thread = threading.Thread(target=self.exec, name="backend")
        self._start_measurement = threading.Event()
        self._stop_measurement = threading.Event()
        self._close_event = threading.Event()
        self._watchdog_event = threading.Event()
        self._thread.start()

        # create a watchdog thread to monitor the backend thread
        self._last_data_time = time.time()
        self._watchdog_thread = threading.Thread(target=self._data_watchdog, name="watchdog", args=(TIMEOUT_S,))
        self._watchdog_thread.start()

        self._gui.set_start_button_callback(self._start_button_callback)
        self._gui.set_close_callback(self._close_callback)

    def _data_watchdog(self, timeout:int = 5):
        """Checks periodically if new data is being received."""
        while not self._close_event.is_set():
            time.sleep(timeout)
            if self._executing_measurement and self._connected:
                if time.time() - self._last_data_time > timeout:
                    self._gui.log_message("No data received for a while, stopping measurement. Please check the connection.")
                    self._watchdog_event.set()

    def _start_button_callback(self, checked_state: bool):
        if checked_state: # button is checked now -> start everything
            self._start_measurement.set()
        else: # button is unchecked now -> stop / reset everything
            self._stop_measurement.set()

    def _close_callback(self):
        self._close_event.set()

    def _init_measurement(self):
        try:
            self._dataAcquirer.set_serial_port(self._gui.get_selected_serial_port())
            self._dataAcquirer.set_baudrate(self._gui.get_selected_baudrate())
            self._dataAcquirer.connect(TIMEOUT_S)
            self._connected = True
        except Exception as e:
            self._gui.log_message(f"Error connecting to data acquirer: {e}")
            self._connected = False
            return

        try:
            self._pipeline = self._pipeline_builder.build_pipeline(self._gui.get_selected_mesh_type(),
                                                                   self._gui.get_selected_number_of_electrodes(),
                                                                   self._gui.get_selected_h0(),
                                                                   None,
                                                                   self._gui.get_selected_injection_pattern())
        except Exception as e:
            self._gui.log_message(f"Error while creating the pipeline: {e}")
            return
        if self._pipeline is None:
            raise RuntimeError("Pipeline is not set.")
        self._executing_measurement = True

    def _end_measurement(self):
        self._disconnect_data_acquirer()
        self._executing_measurement = False

    def _disconnect_data_acquirer(self):
        if self._connected:
            try:
                self._dataAcquirer.disconnect()
                self._gui.log_message('Disconnected from data acquirer.')
            except Exception as e:
                self._gui.log_message(f"Error disconnecting from data acquirer: {e}")
            self._gui.log_message('Measurement stopped.')
            self._connected = False

    def exec(self):
        try:
            # fill all drop down menus in the gui with data
            self._gui.set_meshtypes(self._registry.get_meshtypes())
            self._gui.set_serial_ports(self._dataAcquirer.get_serial_ports())
            self._gui.set_available_baudrates(self._dataAcquirer.get_available_baudrates())
            self._gui.set_available_electrode_numbers([number for number in ElectrodeNumber])
            self._gui.set_available_injection_patterns([pattern for pattern in InjectionPattern])

            while True:
                # evaluate all flags
                if self._close_event.is_set():
                    self._disconnect_data_acquirer()
                    break # terminate thread

                if self._start_measurement.is_set():
                    self._start_measurement.clear()
                    self._init_measurement()

                if self._stop_measurement.is_set():
                    self._stop_measurement.clear()
                    self._end_measurement()

                if self._watchdog_event.is_set():
                    self._watchdog_event.clear()
                    self._gui.log_message("Watchdog triggered, stopping measurement.")
                    self._end_measurement()

                # execution of measurement
                if self._executing_measurement and self._connected:
                    voltages = self._dataAcquirer.acquire_data(timeout=TIMEOUT_S)
                    data = self._pipeline.evaluate_data(voltages)

                    self._gui.update_heat_map(data, self._pipeline.mesh.el_pos, self._pipeline.mesh.meshObject)
                    self._gui.update_voltage_plot(voltages)
                    anomaly_position = self._pipeline.get_anomaly_position()

                    self._gui.set_anomaly_position(anomaly_position)
                time.sleep(0.1)
                self._last_data_time = time.time()

        except Exception as e:
            raise RuntimeError(f"Backend got unexpected exception: {e}")
