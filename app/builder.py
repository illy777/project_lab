# Copyright (c) 2025 
# SPDX-License-Identifier: MIT
# Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
#
# Descritpion: This module contains the measurement registry for the EIT system.

from pipelines.circular_mesh import *
from pipelines.registry import *

class Pipeline_Builder:
    def __init__(self):
        self.registry = Pipeline_Registry()
        if self.registry is None:
            raise ValueError("Registry is not provided. Please provide a valid registry.")

    def _validate_meshtype(self, meshtype):
        meshtypes = self.registry.get_meshtypes()
        if meshtype not in meshtypes:
            raise ValueError(f"Invalid meshtype: {meshtype}. Available meshtypes are: {meshtypes}")

    def build_pipeline(self, meshtype: str, n_el: int, h0: float, maxArea: float, data_interface: Data_Acquirer) -> Pipeline:
        self._validate_meshtype(meshtype)
        for key, choose_func in self.registry.meshoptions.items():
            if key == meshtype:
                pipeline = choose_func(n_el, h0, maxArea)
                pipeline.set_data_interface(data_interface)
                break
        if pipeline is None:
            raise ValueError("Measurement object is not initialized. Please check the meshtype and parameters.")
        if not callable(pipeline.do_measurement):
            raise ValueError("Measurement method is not callable. Please implement the method do_measurement(self, data:np.ndarray)-> np.ndarray in the measurement class.")
        return pipeline
