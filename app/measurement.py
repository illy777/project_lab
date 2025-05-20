#Author: Isaac Lucas de Lima Yuki <isaacyuki@hotmail.com>
#Descritpion: This module contains the measurement registry for the EIT system.

from pipelines.circular_mesh import *
from pipelines.registry import *


class Measurement:
    def __init__(self, meshtype: str, n_el: int = None, h0: float = None, maxArea: float = None, registry: Pipe_Registry = None):
        self.registry = registry
        if registry is None:
            raise ValueError("Registry is not provided. Please provide a valid registry.")
        self.meshtype = meshtype
        self.mesh = None
        self.measurement = None
        if not self._validate_meshtype():
            raise ValueError(f"Invalid meshtype: {self.meshtype}")
        self._choose_measurement(n_el, h0, maxArea)

    def _validate_meshtype(self):
        meshtypes = self.registry.get_meshtypes()
        return self.meshtype in meshtypes

    def _choose_measurement(self, n_el: int, h0: float, maxArea: float):
        for key, choose_func in self.registry.meshoptions.items():
            if key == self.meshtype:
                choice = choose_func(n_el, h0, maxArea)
                self.mesh = choice.mesh
                self.measurement = choice.measurement
                break
        if self.mesh is None:
            raise ValueError("Mesh object is not initialized. Please check the meshtype and parameters.")
        if self.measurement is None:
            raise ValueError("Measurement object is not initialized. Please check the meshtype and parameters.")
        if not callable(self.measurement.do_measurement):
            raise ValueError("Measurement method is not callable. Please implement the method do_measurement(self, data:np.ndarray)-> np.ndarray in the measurement class.")

    def do_measurement(self, data: np.ndarray) -> np.ndarray:
        return self.measurement.do_measurement(data)
    
