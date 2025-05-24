# Copyright (c) 2025 
# SPDX-License-Identifier: MIT
# Author: Thomas Harald Reinhard RUBIN <thomas.rubin2@protonmail.com>
#
# Descritpion: This module is the main Interface between the GUI and the backend EIT system.
# This module is the overseer for the EIT system, managing the GUI, data acquisition, and pipeline execution.
from abc import abstractmethod
from abc import ABC
import time
from app.factory import Pipeline
from app.data_types import MeshType, InjectionPattern, ReconstructionAlgorithm

import numpy as np

class GuiInterface():

    @abstractmethod
    def get_number_of_electrodes(self) -> int:
        pass

    @abstractmethod
    def get_h0(self) -> float:
        pass

    @abstractmethod
    def get_selected_mesh_type(self) -> MeshType:
        pass

    @abstractmethod
    def get_max_area(self) -> float:
        pass

    @abstractmethod
    def get_injection_pattern(self) -> InjectionPattern:
        pass

    @abstractmethod
    def get_reconstruction_algorithm(self) -> ReconstructionAlgorithm:
        pass

    @abstractmethod
    def set_start_button_callback(self, callback: callable):
        pass

    @abstractmethod
    def set_meshtypes(self, meshtypes: list[MeshType]):
        pass

    @abstractmethod
    def log_message(self, message: str):
        pass

    @abstractmethod
    def set_anomaly_position(self, anomaly_position: int):
        pass

    @abstractmethod
    def update_heat_map(self, data, el_position: int, mesh_object):
        pass

    @abstractmethod
    def update_voltage_plot(self, voltages_V: np.ndarray, frequency_Hz: float = 10):
        pass

class DataAcquirer(ABC):
    @abstractmethod
    def acquire_data(self) -> np.ndarray:
        """This method should be implemented in the derived class."""
        pass

class PipelineBuilderInterface(ABC):
    @abstractmethod
    def build_pipeline(self, meshtype: MeshType, n_el: int, h0: float, maxArea: float) -> Pipeline:
        pass

class RegistryInterface(ABC):
    @abstractmethod
    def get_meshtypes(self) -> list[MeshType]:
        pass

class Overseer:
    def __init__(self, gui_interface: GuiInterface, data_acquirer_interface: DataAcquirer,
                 pipeline_builder_interface: PipelineBuilderInterface,
                 registry_interface: RegistryInterface):
        self._gui = gui_interface
        self._dataAcquirer = data_acquirer_interface
        self._pipeline_builder = pipeline_builder_interface
        self._registry = registry_interface

        self._pipeline = None

        self._executing_measurement: bool = False
        self._start_measurement: bool = False
        self._gui.set_start_button_callback(self.start_button_callback)

    def start_button_callback(self, checked_state: bool):
        self._executing_measurement = checked_state
        self._start_measurement = checked_state

    def exec(self):
        # get all implemented meshtypes and feed to gui, only reloads when restarted
        self._gui.set_meshtypes(self._registry.get_meshtypes())

        while True:
            if self._start_measurement:
                meshtype = self._gui.get_selected_mesh_type()
                number_electrods = self._gui.get_number_of_electrodes()
                h0 = self._gui.get_h0()

                self._pipeline = self._pipeline_builder.build_pipeline(meshtype, number_electrods, h0, maxArea=None)
                loop_count = 0
                self._start_measurement = False
            while self._executing_measurement:
                voltages = self._dataAcquirer.acquire_data()
                if self._pipeline is None:
                    raise RuntimeError("Pipeline is not set.")
                data = self._pipeline.evaluate_data(voltages)

                self._gui.update_heat_map(data, self._pipeline.mesh.el_pos, self._pipeline.mesh.meshObject)
                self._gui.update_voltage_plot(voltages)
                anomaly_position = self._pipeline.get_anomaly_position()
                
                self._gui.set_anomaly_position(anomaly_position)
            time.sleep(0.1)